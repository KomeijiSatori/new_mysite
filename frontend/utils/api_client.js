import axios from 'axios';

class ApiClient {
    get_axios_client () {
        let axios_client = axios.create(this.client_config);
        axios_client.interceptors.response.use(function (response) {
            if (response.status !== 200) {
                return Promise.reject(response.data);
            }
            return response.data;
        }, function (error) {
            error = error.response || error;
            console.log('error', error);
            if (!error.status) {
                return Promise.reject({
                    code: 999,
                    message: 'Server Error!',
                });
            }
            var message = '';
            if (error.status >= 400 && error.status < 500) {
                message = 'request error, message: ' + error.status + ': ' + error.statusText + '. ' + error.data.message;
            } else if (error.status === 502 || error.status === 504) {
                message = 'The server is busy or restarting';
            } else {
                message = 'Internal Server Error';
            }
            return Promise.reject({
                code: 999,
                message: message,
            });
        });
        return axios_client;
    }
    constructor (config) {
        this.client_config = config;
        this.client = this.get_axios_client();
    }
    get (url, params, config) {
        let mergedConfig = Object.assign({}, config, this.client_config, {url: url, params: params, method: 'get'});
        return this.request(mergedConfig);
    }
    post (url, data, config) {
        let mergedConfig = Object.assign({}, config, this.client_config, {url: url, data: data, method: 'post'});
        return this.request(mergedConfig);
    }
    request (config) {
        return this.client.request(config)
            .then(response => {
                return response;
            })
            .catch(response => {
                console.log('Error Occurs. Response: ' + response);
                return Promise.reject(response);
          });
    }
}

export default ApiClient;
