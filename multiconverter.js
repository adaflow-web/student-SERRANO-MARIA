const prompt = require('prompt-sync')()
var start = prompt("Do you want to convert a value? yes/no ")
if (start == yes){
    var value = prompt("Which conversion? (euros/celsius/inches)")
        if(value == "euros"){
            console.log(exchange(euros))
        }else if(value == "celsius"){
            console.log(temp_conv(celsius))
        }else if(value== "inches"){
            console.log(inchTocm())
        }
}else{
    process.exit()
}

function exchange(euros){
    return euros + " euros are " + (euros*0.98).toString() + " CHF"
}

function temp_conv(celsius){
    msg_1 = " degrees Celsius are "
    msg_2 = " degrees Farenheit"
    result = celsius * 9/5 +32
    return celsius.toString() + msg_1 + result.toString() + msg_2
}

function inchTocm(){
    var inches = prompt("Enter a number: ")
    var result = parseFloat(inches) * 2.54
    var message = inches + " inches are " + result + " cm"
    return message
}

function mensaje() {
    let Edad = document.getElementById("edadUsuario").value

if (Edad >=18) {
    alert("Eres mayor de edad")
    return
}
else {
    alert("Eres menor de edad")
    return
}
}