
document.addEventListener("DOMContentLoaded", function(){
    if (window.location.pathname == '/profile'){
        var change_btn = document.querySelector("#change_btn");
        var sub_btn = document.querySelector("#submit_btn");
        var delete_btn = document.querySelector("#delete_btn");
        var input_name = document.querySelector("#name");
        var input_mail = document.querySelector("#mail");
        var back_arrow = document.querySelector(".back-arrow");
        var prev_password = document.querySelector("#prev_password");
        var new_password = document.querySelector("#new_password");
        change_btn.addEventListener("click", function(){
            input_name.removeAttribute("readonly");
            input_name.removeAttribute("disabled");
            input_mail.removeAttribute("readonly");
            input_mail.removeAttribute("disabled");
            change_btn.setAttribute("hidden", "");
            sub_btn.removeAttribute("hidden");
            prev_password.removeAttribute("hidden");
            new_password.removeAttribute("hidden");
            delete_btn.setAttribute("hidden", "");
            back_arrow.removeAttribute("hidden");
});
}
});



