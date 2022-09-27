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
)

func homePage(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Welcome to the HomePage!\r\n")
	fmt.Println("Endpoint Hit: homePage")
}

func checkType(v any, t string) {
	fmt.Printf("TYPEOF "+t+": %T\nVALUE: %s\n\n", v, v)
}

func gasMeter(w http.ResponseWriter, r *http.Request) {
	fmt.Println("method:", r.Method) //get request method
	if r.Method == "GET" {
		t, _ := template.ParseFiles("gasmeter.gtpl")
		t.Execute(w, nil)
	} else {
		r.ParseForm()
		// logic part of log in
		fmt.Println("meter:", r.Form["meter"])
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

		topic := os.Getenv("MQTT_TOPIC")
		metvalue, err := strconv.ParseFloat(r.Form["meter"][0], 64)

		payload := map[string]interface{}{
			"cubicmeters": metvalue,
		}
		jsonData, err := json.Marshal(payload)

		if err != nil {
			fmt.Printf("could not marshal json: %s\n", err)
			return
		}
		fmt.Printf("json data: %s\n", jsonData)
		// fmt.Printf("%v", r.Form)
		token = client.Publish(topic, 0, false, jsonData)
		token.Wait()
		time.Sleep(time.Second)
		client.Disconnect(100)
		fmt.Fprintf(w, "Reading sent!\r\n")
	}

}

func handleRequests() {
	http.HandleFunc("/", homePage)
	http.HandleFunc("/gaseo", gasMeter)
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
