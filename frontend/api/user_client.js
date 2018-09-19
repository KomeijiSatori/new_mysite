import BaseApiClient from './base_api_client';

class UserClient extends BaseApiClient {
    constructor() {
        const sub_url = 'user/';
        super(sub_url);
    }

    async login (payloads) {
        const url = 'login/';
        return await this.client.post(url, payloads);
    }

    async logout () {
        const url = 'logout/';
        return await this.client.get(url);
    }

    async get_user_info () {
        const url = 'user_info/';
        return await this.client.get(url);
    }
}

export default new UserClient();
