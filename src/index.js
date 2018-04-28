import Vue from "vue";
import firebase from "firebase";
import "./pwa";
import store from "./modules/store";
import router from "./modules/router";
import fontawesome from "@fortawesome/fontawesome";
import icons from "@fortawesome/fontawesome-free-solid";
import css from "./app.scss";
import Nav from "./components/Nav.vue";
firebase.initializeApp({
	apiKey: "AIzaSyDZGcrdh48alSZlUoiQSpXP0fktcVPJf2w",
	authDomain: "talanx-hack.firebaseapp.com",
	databaseURL: "https://talanx-hack.firebaseio.com",
	projectId: "talanx-hack",
	storageBucket: "talanx-hack.appspot.com",
	messagingSenderId: "784808067653"
});

const app = new Vue({
	el: "#app",
	router,
	store,
	render() {
		return (
			<div class="app-container">
				<transition name="fade" mode="out-in">
					<router-view />
				</transition>
				<Nav />
			</div>
		);
	}
});
