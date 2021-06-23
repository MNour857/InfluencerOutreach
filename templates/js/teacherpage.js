var data = {
    username : "tabish",
    password : "tabish1212" 
}
function Login(){
            var user_name = document.getElementById("name").value
            var _password =  document.getElementById("pass").value 
         if(data["username"] == user_name && data["password"] == _password){
            window.location.href = "teacherpage.html"
        } else if(user_name == "" && _password == ""){
            alert('Please fill info!!!')
        }
        else{
            alert('Invalid Email or Password')
        }

}

function openprofile(){
    document.querySelector(".profile").style.display = "block";
    document.querySelector(".stp").style.display= "none"
}
function openstdprf(){
    document.querySelector(".stp").style.display= "block";
    document.querySelector(".profile").style.display = "none";
}

function openPage(v){
    window.location.href=v
}

function openprf(){
    document.getElementsByClassName(".prf").value
    window.location="student/studentpage.html"
}