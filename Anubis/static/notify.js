document.getElementById("button").addEventListener('click', function(){
    document.querySelector('.bg-modal').style.display = 'flex';
});

document.querySelector('.close').addEventListener('click', function(){
    document.querySelector('.bg-modal').style.display = 'none';
});



const BtnAdd = document.querySelector(".btn-add");
const DivContainer = document.getElementById("div-container");

BtnAdd.addEventListener("click", AddNew);

function AddNew() {
  const newDiv = document.createElement("div");
  console.log("add");
  newDiv.classList.add("div-shadow");
  DivContainer.appendChild(newDiv);
}

// Pop up for Camera1 POST

function openForm() {
  document.getElementById("camera1").style.display = "block";
}

function closeForm() {
  document.getElementById("camera1").style.display = "none";
}


// Pop Up for Camera2 POST

function cam2form() {
  document.getElementById("camera2").style.display = "block";
}

function closecam2Form() {
  document.getElementById("camera2").style.display = "none";
}


//Popup for Camera3 POST

function cam3form() {
  document.getElementById("camera3").style.display = "block";
}

function closecam3Form() {
  document.getElementById("camera3").style.display = "none";
}


