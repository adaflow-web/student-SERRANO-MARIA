const button = document.getElementById("myButton")
const input = document.getElementById("myText")
const content= document.getElementById("content")
const buttonRemove = document.getElementById("buttonRemove")

function addParagraph(){  
    const newParagraph = document.createElement("p")
    newParagraph.innerText = myText.value;
    newParagraph.className = "color"
    content.appendChild(newParagraph)
}


const button2 = document.getElementById("myButton2")
const input2 = document.getElementById("myText2")


function addParagraph2(){  
    const newParagraph2 = document.createElement("p")
    newParagraph2.innerText = myText2.value;
    newParagraph2.className = "color"
    content.appendChild(newParagraph2)
}

function removeLastPara(){
    const paragraphs = document.getElementsByClassName("color")
    if(paragraphs.length >0){
        content.removeChild(paragraphs[paragraphs.length -1])
    }
}

button.addEventListener("click", addParagraph)
button2.addEventListener("click", addParagraph2 )
buttonRemove.addEventListener("click", removeLastPara)