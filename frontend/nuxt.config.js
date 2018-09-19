module.exports = {
    build: {
        vendor: ['~/plugins/iview']
    },
    plugins: ['~/plugins/iview'],
    css: [
        'iview/dist/styles/iview.css',
    ],
    router: {
        middleware: 'check_auth',
    },
    // iview-loader
    extend (config) {
        config.module.rules.push({
            test: /\.vue$/,
            loader: 'iview-loader',
            options: {
                prefix: false
            }
        })
    },
    modules: [
    ],
    loading: { color: '#3B8070' },
}
