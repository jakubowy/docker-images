<!DOCTYPE html>
<html>

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        .center {
            margin: 0;
            position: absolute;
            top: 50%;
            left: 50%;
            -ms-transform: translate(-50%, -50%);
            transform: translate(-50%, -50%);
        }
    </style>
</head>

<body>
    <center>
        <div class="center">
            <h3>
                <form method="post">
                    <label for="topic">Choose a topic:</label>
                    <select id="topic" name="topic">
                        <option value="6g4l">Gas</option>
                        <option value="energa-ucka">Electricity Ucka</option>
                        <option value="water-main-ucka">Water main Ucka</option>
                        <option value="water-garden-ucka">Water garden Ucka</option>
                        <option value="water-cold-pop">Water cold</option>
                        <option value="water-hot-pop">Water hot</option>
                        <option value="testtest">Test</option>
                    </select>
                    <p>
                        <label for="reading">Stan licznika:</label>
                        <input id="reading" type="number" step="0.001" name="reading">
                    <p>
                        <input type="submit" value="Submit">
                </form>
            </h3>
        </div>
    </center>
</body>

</html>
