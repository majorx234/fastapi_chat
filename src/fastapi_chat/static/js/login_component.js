import {httpPostFetch} from "./http_operation.js";
import "./forge-sha256.min.js"
import * as bootstrap from "../bootstrap-5.3.1-dist/bootstrap.min.js"


const template = document.createElement("template");
template.innerHTML = `
<style>
  .image-container {
      height: 100%;
    }

  .image-container img {
    max-width: 90%;   /* Bild passt sich der Breite an */
    max-height: 90%;  /* Bild passt sich der Höhe an */
    object-fit: contain; /* keine Verzerrung */
    border-radius: 12px; /* optional, für weiche Ecken */
    box-shadow: 0 4px 15px rgba(0,0,0,0.3); /* optional, schöner Effekt */
  }
</style>

<meta name="viewport" content="width=device-width, initial-scale=1">
<link href="./bootstrap-5.3.1-dist/bootstrap.min.css" rel="stylesheet">
<div class="d-flex flex-row align-items-center" data-bs-theme="light">
  <div class="card login-card p-4 shadow" style="width: 100%; max-width: 320px;">
    <!-- logo -->
    <img src="logo.png" alt="logo">

    <h3 class="text-center mb-3">Login</h3>
    <form id="loginForm">
      <div class="form-group">
        <label class="form-label" for="username">User Name:</label>
        <input type="text" id="user_name_input" class="form-control form-control-sm" placeholder="User" required>
      </div>
      <div class="form-group">
        <label class="form-label" for="password">Password:</label>
        <input type="password" class="form-control form-control-sm" id="password_input" placeholder="Enter password" required>
      </div>
       <button type="button" class="btn btn-primary" id="login_button">login</button>
    </form>
    <div class="text-center mt-3">
      <a href="#" class="mr-3">Forgot Password?</a>
      <a href="#">Sign Up</a>
    </div>
  </div>
</div>
`;

/**
 * Class constructor of derived class
 * Let component be a Shadow DOM
 * Initializes token
 */
class LoginComponent extends HTMLElement {
    constructor() {
        super();
        this._token = null;
        this._end_point_name = "login/post_user_psw";
        this.root = this.attachShadow({mode: "closed"});
        this.root.appendChild(template.content.cloneNode(true));
        this.root.querySelector("#login_button").onclick = () => {
            this.httpPostLogin();
        };
    }

    logEvent(log_msg) {
        this.dispatchEvent(new CustomEvent("log-event",{detail : log_msg} ));
    }

    tokenEvent(token_msg) {
        this.dispatchEvent(new CustomEvent("token-event",{detail : token_msg} ));
    }

    httpPostUserForLogin(){
        let login_form = this.root.querySelector("#loginForm");
        let user_name = this.root.querySelector("#user_name_input").value;
        let password = this.root.querySelector("#password_input").value;
        console.log('Username:', user_name);
        console.log('Password:', password);

        // TODO salt as attribute
        let salt = "salt29562"
        let password_hash = forge_sha256(password + salt);

        if(user_name == "" || password == "") {
            alert("Both fields are required!");
        } else {
            let variable_context = "login_data: ";
            let response_handler = (response_text) => {
                let json_object_data = JSON.parse(response_text);
                this.global_token = json_object_data["token"];
                this.tokenEvent(this.global_token);
                this.logEvent(variable_context + response_text);
            };
            let json_object_data = {
                username : user_name,
                hashed_password : password_hash
            };
            let json_string = JSON.stringify(json_object_data);
            httpPostFetch(this._end_point_name, json_string, variable_context, response_handler, null, 'json');
        }
    }

    /**
     * Lifecycle hook fires each time the webcomponent is appended into a document-connected element
     * Sets onclick events on buttons and sets methods which are automatically called when component got loaded
     */
    connectedCallback() {

        this.root.querySelector("#login_button").onclick = (event) => {
            event.preventDefault();
            this.httpPostUserForLogin();
        };
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (name === "token"){
            if (oldValue !== newValue) {
                this._token = newValue;
            }
        }
    }
    /* getter setter */
    get token() {
        return this.getAttribute("token");
    }
    set token(val) {
        this.setAttribute("token", val);
        this._token = val;
    }
}

customElements.define("login-component", LoginComponent);
