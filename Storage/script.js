const content = document.getElementById("content")
const buttonAdd = document.getElementById("add")
const buttonRemove = document.getElementById("remove")
const buttonClear = document.getElementById("clear")


const globalArray = [];

function addItem() {
    const input = document.getElementById("myText").value
    globalArray.push(input)
    console.log(globalArray)
    localStorage.setItem("contentLocal", globalArray)

    const newPara = document.createElement("p")
    newPara.innerText = myText.value
    content.appendChild(newPara)
    myText.value = ""
}

buttonAdd.addEventListener("click", addItem)
document.addEventListener('DOMContentLoaded', () => {
    if (localStorage.length !== 0) {
        const array = localStorage.getItem("contentLocal").split(',');
        if (array[0] != "") {
            for (let index = 0; index < array.length; index++) {
                const newPara = document.createElement("p")
                newPara.innerText += array[index]
                content.appendChild(newPara);
                globalArray.push(array[index])
            }
        }
    }
})


function clearAll() {
    const div = document.getElementById("content");
    console.log(div.children)
    while (div.children.length > 0) {
        div.removeChild(div.firstChild);
    }
    localStorage.clear()
    globalArray.length = 0
}
buttonClear.addEventListener("click", clearAll)

function removeItem() {
    const div = document.getElementById("content");

    if (globalArray.length > 0) {
        globalArray.pop()
        localStorage.setItem("contentLocal", globalArray)
    }
    if (div.children.length > 0) {
        div.removeChild(div.lastChild)
    }
}
buttonRemove.addEventListener("click", removeItem)   
