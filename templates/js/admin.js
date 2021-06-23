var data = 
    {
        username : "tabish",
        password : "tabish1212"
    }

function login(){
    var user_name = document.getElementById("username").value
    var _password =  document.getElementById("password").value


    if((data["username"] == user_name) && (data["password"] == _password)){
        
        window.location ="adminpage/adminpage.html";
        
}else if(user_name == "" && _password == ""){
    alert('please fill the data')
}

else{
    alert('Invalid Email or Password')
}

}
function openPage(v){
    window.location.href=v
}
function _add(v){
    if (v=="stu"){
        addstd()
    }else if(v=="teacher"){
        addteacher()
    }
}

function addstd(){
document.querySelector(".adstd").style.display = "block";
document.querySelector(".addteacher").style.display = "none";
document.querySelector(".dltsrch").style.display="none";
document.querySelector(".dlttchr").style.display="none";
document.querySelector(".gwc").style.display="none";
document.querySelector(".fp").style.display="none";
document.querySelector(".ims").style.display="none";
document.querySelector(".ted").style.display="none";
document.querySelector(".stdd").style.display="none";
}
function addteacher(){
    document.querySelector(".addteacher").style.display = "block";
    document.querySelector(".adstd").style.display = "none";
    document.querySelector(".dltsrch").style.display="none";
    document.querySelector(".dlttchr").style.display="none";
    document.querySelector(".gwc").style.display="none";
    document.querySelector(".fp").style.display="none";
    document.querySelector(".ims").style.display="none";
    document.querySelector(".ted").style.display="none";
    document.querySelector(".stdd").style.display="none";
}
function dlt(v){
    if(v=="teacher"){
        dlttchr()
    }else if(v=="std"){
        dltsrch()
    }
}
function dltsrch(){
    document.querySelector(".dltsrch").style.display="block";
    document.querySelector(".adstd").style.display = "none";
    document.querySelector(".addteacher").style.display = "none";
    document.querySelector(".dlttchr").style.display="none";
    document.querySelector(".gwc").style.display="none";
    document.querySelector(".fp").style.display="none";
    document.querySelector(".ims").style.display="none";
    document.querySelector(".ted").style.display="none";
    document.querySelector(".stdd").style.display="none";
}
function dlttchr(){
    document.querySelector(".dlttchr").style.display="block";
    document.querySelector(".adstd").style.display = "none";
    document.querySelector(".addteacher").style.display = "none";
    document.querySelector(".dltsrch").style.display="none";
    document.querySelector(".gwc").style.display="none";
    document.querySelector(".fp").style.display="none";
    document.querySelector(".ims").style.display="none";
    document.querySelector(".ted").style.display="none";
    document.querySelector(".stdd").style.display="none";
}
function view(v){
    if(v=="gwc"){
        gwc()
    }
    else if(v=="fp"){
        fp()
    }
    else if(v=="ims"){
        ims()
    }
    else if(v=="ted"){
        ted()
    }
    else if(v=="stdd"){
        stdd()
    }
}
function gwc(){
    document.querySelector(".gwc").style.display="block";
    document.querySelector(".dlttchr").style.display="none";
    document.querySelector(".adstd").style.display = "none";
    document.querySelector(".addteacher").style.display = "none";
    document.querySelector(".dltsrch").style.display="none";
    document.querySelector(".fp").style.display="none";
    document.querySelector(".ims").style.display="none";
    document.querySelector(".ted").style.display="none";
    document.querySelector(".stdd").style.display="none";
}
function fp(){
    document.querySelector(".fp").style.display="block";
    document.querySelector(".gwc").style.display="none";
    document.querySelector(".dlttchr").style.display="none";
    document.querySelector(".adstd").style.display = "none";
    document.querySelector(".addteacher").style.display = "none";
    document.querySelector(".dltsrch").style.display="none";
    document.querySelector(".ims").style.display="none";
    document.querySelector(".ted").style.display="none";
    document.querySelector(".stdd").style.display="none";
}
function ims(){
    document.querySelector(".ims").style.display="block";
    document.querySelector(".fp").style.display="none";
    document.querySelector(".gwc").style.display="none";
    document.querySelector(".dlttchr").style.display="none";
    document.querySelector(".adstd").style.display = "none";
    document.querySelector(".addteacher").style.display = "none";
    document.querySelector(".dltsrch").style.display="none";
    document.querySelector(".ted").style.display="none";
    document.querySelector(".stdd").style.display="none";
}
function ted(){
    document.querySelector(".ted").style.display="block";
    document.querySelector(".ims").style.display="none";
    document.querySelector(".fp").style.display="none";
    document.querySelector(".gwc").style.display="none";
    document.querySelector(".dlttchr").style.display="none";
    document.querySelector(".adstd").style.display = "none";
    document.querySelector(".addteacher").style.display = "none";
    document.querySelector(".dltsrch").style.display="none";
    document.querySelector(".stdd").style.display="none";
}
function stdd(){
    document.querySelector(".stdd").style.display="block";
    document.querySelector(".ted").style.display="none";
    document.querySelector(".ims").style.display="none";
    document.querySelector(".fp").style.display="none";
    document.querySelector(".gwc").style.display="none";
    document.querySelector(".dlttchr").style.display="none";
    document.querySelector(".adstd").style.display = "none";
    document.querySelector(".addteacher").style.display = "none";
    document.querySelector(".dltsrch").style.display="none";
}