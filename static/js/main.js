document.addEventListener("DOMContentLoaded", function () {

```
console.log("Event Registration Portal Loaded Successfully");

// ==========================
// Fade In Animation
// ==========================

document.body.style.opacity = "0";

setTimeout(() => {

    document.body.style.transition = "opacity 0.8s";
    document.body.style.opacity = "1";

}, 100);


// ==========================
// Delete Confirmation
// ==========================

const deleteButtons = document.querySelectorAll(".btn-danger");

deleteButtons.forEach(button => {

    button.addEventListener("click", function (event) {

        const confirmDelete = confirm(
            "Are you sure you want to delete this registration?"
        );

        if (!confirmDelete) {

            event.preventDefault();

        }

    });

});


// ==========================
// Button Hover Animation
// ==========================

const buttons = document.querySelectorAll(".btn");

buttons.forEach(btn => {

    btn.addEventListener("mouseover", () => {

        btn.style.transform = "scale(1.05)";
        btn.style.transition = "0.3s";

    });

    btn.addEventListener("mouseout", () => {

        btn.style.transform = "scale(1)";

    });

});


// ==========================
// Card Hover Animation
// ==========================

const cards = document.querySelectorAll(".card");

cards.forEach(card => {

    card.addEventListener("mouseover", () => {

        card.style.transform = "translateY(-5px)";
        card.style.transition = "0.3s";

    });

    card.addEventListener("mouseout", () => {

        card.style.transform = "translateY(0px)";

    });

});


// ==========================
// Auto Hide Alerts
// ==========================

const alerts = document.querySelectorAll(".alert");

alerts.forEach(alert => {

    setTimeout(() => {

        alert.style.display = "none";

    }, 5000);

});


// ==========================
// Current Year Footer
// ==========================

const footerYear = document.getElementById("currentYear");

if (footerYear) {

    footerYear.innerText =
        new Date().getFullYear();

}


// ==========================
// Registration Form Validation
// ==========================

const form = document.querySelector("form");

if (form) {

    form.addEventListener("submit", function (e) {

        const name =
            document.querySelector(
                "input[name='name']"
            );

        const email =
            document.querySelector(
                "input[name='email']"
            );

        const phone =
            document.querySelector(
                "input[name='phone']"
            );

        if (
            name &&
            email &&
            phone
        ) {

            if (
                name.value.trim() === "" ||
                email.value.trim() === "" ||
                phone.value.trim() === ""
            ) {

                alert(
                    "Please fill all fields."
                );

                e.preventDefault();
            }

        }

    });

}
```

});

function animateValue(id,start,end,duration){

    let obj=document.getElementById(id);

    if(!obj) return;

    let range=end-start;

    let current=start;

    let increment=end>start?1:-1;

    let stepTime=Math.abs(
        Math.floor(duration/range)
    );

    let timer=setInterval(function(){

        current+=increment;

        obj.innerHTML=current;

        if(current==end){

            clearInterval(timer);

        }

    },stepTime);

}

animateValue(
    "participants",
    0,
    1000,
    1500
);

// ==========================
// DARK MODE
// ==========================

const darkBtn =
document.getElementById(
"darkModeBtn"
);

if(localStorage.getItem("theme") === "dark"){

    document.body.classList.add(
        "dark-mode"
    );

}

if(darkBtn){

    darkBtn.addEventListener(
    "click",
    ()=>{

        document.body.classList.toggle(
            "dark-mode"
        );

        if(
            document.body.classList.contains(
                "dark-mode"
            )
        ){

            localStorage.setItem(
                "theme",
                "dark"
            );

        }
        else{

            localStorage.setItem(
                "theme",
                "light"
            );

        }

    });

}
window.addEventListener(
"load",
()=>{

    document.getElementById(
        "loader"
    ).style.display="none";

});
function animateValue(
id,
start,
end,
duration
){

    let obj =
    document.getElementById(id);

    if(!obj) return;

    let range=end-start;

    let current=start;

    let increment=1;

    let stepTime=
    duration/range;

    let timer=
    setInterval(()=>{

        current+=increment;

        obj.innerHTML=current+"+";

        if(current>=end){

            clearInterval(timer);

        }

    },stepTime);

}

animateValue(
"participants",
0,
1000,
1500
);
function showToast(message){

    const toastBody =
    document.querySelector(
        ".toast-body"
    );

    if(!toastBody) return;

    toastBody.innerText =
    message;

    const toast =
    new bootstrap.Toast(
        document.getElementById(
            "liveToast"
        )
    );

    toast.show();

}
showToast(
"Welcome Admin!"
);
const menuBtn =
document.getElementById(
"menuBtn"
);

const sidebar =
document.getElementById(
"sidebar"
);

if(menuBtn){

    menuBtn.addEventListener(
    "click",
    ()=>{

        sidebar.classList.toggle(
            "active"
        );

    });

}