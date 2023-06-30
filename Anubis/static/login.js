// pop up for sign-up
function signup() {
    var div = document.getElementById("login-block");
    var signup = document.getElementById("signup-block");
    var button = document.getElementById('button');
    div.style.display = "none";
    signup.style.display = "block";
    signup.style.borderTopColor = "#0384fc";
    button.style.backgroundColor = "#0384fc";
    button.style.borderColor = "#0384fc";
    
}
 
// pop up for login
function login(){
    var div = document.getElementById("login-block");
    var signup = document.getElementById("signup-block");
    signup.style.display = "none";
    div.style.display = "block";
}

// hide if password text and check if password matches
function check(){
    var pass1 = document.getElementById('password1').value;
    var pass2 = document.getElementById('password2').value;
    var message = document.getElementById('passwordcenter');

    if (pass1 === pass2) {
        message.style.display = "none";
    } else {
        message.style.display = "block";
    }

}