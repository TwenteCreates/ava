import Vue from "vue";
import "./pwa";
import router from "./modules/router";
import fontawesome from "@fortawesome/fontawesome";
import icons from "@fortawesome/fontawesome-free-solid";
import css from "./app.scss";
import Nav from "./components/Nav.vue";

const app = new Vue({
	el: "#app",
	router,
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
