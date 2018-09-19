export default function (context) {
    // if the user has login
    console.log("---------cookie----------");
    console.log(context.req.headers.cookie);
    console.log("---------cookie----------");
    // if (!context.store.getters.is_login) {
    //     // load the data from cookie, for auto login
    //     if (context.req.getHeader('set-cookie')) {
            
    //     } else {
            
    //     }
    // }
}
