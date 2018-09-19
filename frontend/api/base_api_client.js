import ApiClient from '@/utils/api_client';

const client_config = {
    baseURL: '/api/',
    timeout: 20000,
};

class BaseApiClient {
    constructor (sub_url) {
        const baseURL = client_config.baseURL + sub_url;
        this.client = new ApiClient({...client_config, baseURL});
    }
}

export default BaseApiClient;
