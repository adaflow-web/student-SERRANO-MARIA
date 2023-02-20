var number = Math.floor((Math.random() * 100) + 1);
    console.log(number)

//const prompt = require('prompt-sync')();

//var start = parseInt(prompt("Type a number from 1 to 100: "))
var start = window.prompt("Type a number from 1 to 100: ")

var result = number
var counter = 0

if(!isNaN(start)){
    while(parseInt(start) != result){
    
        if (start< result){
            console.log("The secret number is bigger. Try again!")
            counter += 1
            var start = window.prompt("type a number from 1 to 100: ") 
            //prompt("Type a number from 1 to 100: ")
            
                if(isNaN(start)){
                    console.log("That's not a number.") 
                    break   
                }
        }else if(parseInt(start)> result){
            console.log("The secret number is smaller. Try again")
            counter += 1
            var start = window.prompt("type a number from 1 to 100: ")
            
                if(isNaN(start)){
                    console.log("That's not a number.")
                    break
            }
        }      
    }
    if(parseInt(start)==result){
        counter += 1
            if(counter == 1){
                console.log("You guessed the secret number in 1 attempt")
            }else{
                console.log("You guessed the secret number in " + counter + " attempts")
            }
    }
}else {
    console.log("That's not a number.")
}

// let start = prompt("Type a number from 1 to 100: ")

// if(!isNaN(start)) { /* Bucle del programa */ }
// else {
//       console.log("Eso no es un número")
// }



// # When starting the game, a secret number between 1 and 100 is generated.
// # The game asks the user to enter a number.
// # The game will tell the user if the secret number is bigger or smaller than the guess.
// # As long as the user doesn't find the secret number, the game continues.
// # As soon as the user finds the secret number, the game stops and tells the user how many attempts it took to win. Make sure to use the right wording (attempt or attempts)
// # In case the user enters anything else than a number, the game should tell that to the user and quit gracefully
