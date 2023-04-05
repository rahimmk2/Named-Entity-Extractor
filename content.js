chrome.runtime.onMessage.addListener(
    function (message, sender, sendResponse) {
        entities = message
        body = document.body.innerHTML;
        colors = {}

        for (i = 0; i < entities.length; i++) {
            txt = entities[i]['text']
            label = entities[i]['label']

            if (colors.hasOwnProperty(label) == false)
                colors[label] = generateColor()

            newTxt = "<span style='background-color: " + colors[label] + ";'>" + txt + "</span>"
            body = body.replace(txt, newTxt);
        }
        document.body.innerHTML = body;
        console.log(colors)

    }
);

function generateColor() {
    r = Math.floor(Math.random() * 256);
    g = Math.floor(Math.random() * 256);
    b = Math.floor(Math.random() * 256);
    color = "rgb(" + r + ", " + g + ", " + b + ")";
    return color;
}