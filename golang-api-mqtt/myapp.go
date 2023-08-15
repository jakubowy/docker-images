package main

import (
	"encoding/json"
	"fmt"
	"html/template"
	"log"
	"net/http"
	"os"
	"strconv"
	"time"
	mqtt "github.com/eclipse/paho.mqtt.golang"
        "github.com/influxdata/influxdb-client-go/v2"
        "strings"
    )

/*
func homePage(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Welcome to the HomePage!\r\n")
	fmt.Println("Endpoint Hit: homePage")
}
*/
func checkType(v any, t string) {
	// Usage: checkType(varName, "varName")
	fmt.Printf("TYPEOF "+t+": %T\nVALUE: %s\n\n", v, v)
}

func handleRequest(w http.ResponseWriter, r *http.Request) {
	fmt.Println("method:", r.Method) //get request method
	if r.Method == "GET" {
		t, _ := template.ParseFiles("gasmeter.gtpl")
		t.Execute(w, nil)
	} else {
		r.ParseForm()
		fmt.Println("form contents:", r.Form)
		fmt.Fprintf(w, "Sending meter!\r\n")
		checkType(os.Getenv("MQTT_BROKER"), "MQTT_BROKER")
		checkType(os.Getenv("MQTT_TOPIC"), "MQTT_TOPIC")

		var broker = "tcp://" + os.Getenv("MQTT_BROKER")

		options := mqtt.NewClientOptions()
		options.AddBroker(broker)
		options.SetClientID("gomqtt")
		options.SetDefaultPublishHandler(messagePubHandler)
		options.OnConnect = connectHandler
		options.OnConnectionLost = connectionLostHandler

		client := mqtt.NewClient(options)
		token := client.Connect()
		if token.Wait() && token.Error() != nil {
			panic(token.Error())
		}
		checkType(r.Form["topic"][0], "TOPIC")
                topicname := strings.Split(r.Form["topic"][0], " ")[0]
		topic := topicname + "/" + r.Form["topic"][0]
		reading, err := strconv.ParseFloat(r.Form["reading"][0], 64)

		payload := map[string]interface{}{
			"reading": reading,
		}
		jsonData, err := json.Marshal(payload)

		if err != nil {
			fmt.Printf("could not marshal json: %s\n", err)
			return
		}
		fmt.Printf("json data: %s\n", jsonData)
		// fmt.Printf("%v", r.Form)
		token = client.Publish(topic, 0, true, jsonData)
		token.Wait()
		time.Sleep(time.Second)
		client.Disconnect(100)
		fmt.Fprintf(w, "Reading sent!\r\n")
                clientinflux := influxdb2.NewClient(os.Getenv("INFLUX_HOST"), os.Getenv("INFLUX_TOKEN"))
                writeAPI := clientinflux.WriteAPI(os.Getenv("INFLUX_ORG"), os.Getenv("INFLUX_BUCKET"))
                metername := strings.Split(r.Form["topic"][0], " ")[0]
                unitvalue := strings.Split(r.Form["topic"][0], " ")[1]
                fmt.Printf("meter: %s   unit: %s\n", metername, unitvalue)
                writeAPI.WriteRecord(fmt.Sprintf("meter,unit=%s %s=%f", unitvalue, metername, reading))
                writeAPI.Flush()
	        fmt.Printf("influx sent")
            }

}

func handleRequests() {
	http.HandleFunc("/", handleRequest)
	//http.HandleFunc("/gaseo", gasMeter)
	log.Fatal(http.ListenAndServe(":80", nil))
}

var messagePubHandler mqtt.MessageHandler = func(client mqtt.Client, msg mqtt.Message) {
	fmt.Printf("Message %s received on topic %s\n", msg.Payload(), msg.Topic())
}

var connectHandler mqtt.OnConnectHandler = func(client mqtt.Client) {
	fmt.Println("Connected")
}

var connectionLostHandler mqtt.ConnectionLostHandler = func(client mqtt.Client, err error) {
	fmt.Printf("Connection Lost: %s\n", err.Error())
}

func main() {
	handleRequests()
}
