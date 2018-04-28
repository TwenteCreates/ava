import Vue from "vue";
import Vuex from "vuex";
import createPersistedState from "vuex-persistedstate";
Vue.use(Vuex);

const store = new Vuex.Store({
	state: {
		messages: []
	},
	mutations: {
		update(state, newState) {
			state.messages = newState;
		}
	},
	plugins: [createPersistedState()]
});

export default store;
