function openwholeMarksheet(){
    document.querySelector(".marks").style.display = 'block';
    document.querySelector(".marksheet").style.display = "none";
    document.querySelector(".profile").style.display = "none";
}
function openmarksheet(){
    document.querySelector(".marksheet").style.display = "block";
    document.querySelector(".marks").style.display = 'none';
    document.querySelector(".profile").style.display = "none";
}
function profile(){
     document.querySelector(".profile").style.display = "block";
     document.querySelector(".marksheet").style.display = "none";
     document.querySelector(".marks").style.display = "none";
}
var data = {
    username : "tabish",
    password : "tabish1212" 
}
function login(){
            var user_name = document.getElementById("name").value
            var _password =  document.getElementById("pass").value 
            
        if(data["username"] == user_name && data["password"] == _password){
            window.location = "studentpage.html"
        }
        else if(user_name == "" && _password == ""){
            alert('Please Fill the information !!!')
        }
        else{
            alert('Invalid Email or Password')
        }

}
function openPage(v){
    window.location.href=v
}