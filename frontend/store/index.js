import Vue from "vue"
import Vuex from "vuex"

Vue.use(Vuex)

const store = () => new Vuex.Store({
    state: {
        user_info: {
            user_name: '',
            user_id: '',
        },
    },
    getters: {
        is_login: state => {
            return state.user_info.user_name !== '' && state.user_info.user_id !== '';
        }
    },
    mutations: {
        // the payload of mutation should be no more than one
        login (state, user_info) {
            state.user_info.user_name = user_info.user_name;
            state.user_info.user_id = user_info.user_id.toString();
        },
        logout (state) {
            state.user_info.user_name = '';
            state.user_info.user_id = '';
        }
    }
})

export default store
