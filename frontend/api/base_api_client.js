import ApiClient from '@/utils/api_client';

const client_config = {
    baseURL: process.server ? 'http://127.0.0.1/api/' : '/api/',
    timeout: 20000,
    withCredentials: true,
};

class BaseApiClient {
    constructor (sub_url) {
        const baseURL = client_config.baseURL + sub_url;
        this.client = new ApiClient({...client_config, baseURL});
    }
}

export default BaseApiClient;
