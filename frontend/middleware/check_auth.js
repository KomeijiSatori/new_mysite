import UserClient from '@/api/user_client';

export default function (context) {
    if (!context.store.getters.is_login) {
        // get user info by ajax call
        // return a promise to tell nuxt server to wait
        let headers = {}
        if (process.server) {
            // parse the client's header to server to allow server to get data
            headers = {'Cookie' : context.req.headers.cookie}
        }
        return UserClient.get_user_info(headers)
        .then(rsp => {
            if (rsp.code == 0) {
                context.store.commit("login", {
                    user_name: rsp.data.user_name,
                    user_id: rsp.data.user_id,
                });
            }
        })
        .catch(err => {
            console.log(err);
        });
    }
}
