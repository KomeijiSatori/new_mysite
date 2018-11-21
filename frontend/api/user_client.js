import BaseApiClient from './base_api_client';

class UserClient extends BaseApiClient {
    constructor() {
        const sub_url = 'user/';
        super(sub_url);
    }

    login (payloads) {
        const url = 'login/';
        return this.client.post(url, payloads);
    }

    logout () {
        const url = 'logout/';
        return this.client.get(url);
    }

    get_user_info (headers={}) {
        const url = 'user_info/';
        return this.client.get(url, {}, { headers: headers });
    }
}

export default new UserClient();
