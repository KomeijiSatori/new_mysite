<template>
    <div>
        <nuxt/>
    </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
import UserClient from '@/api/user_client';

export default {
    mounted () {
        if (!this.is_login) {
            UserClient.get_user_info().then(rsp => {
                if (rsp.code == 0) {
                    this.$store.commit("login", {
                        user_name: rsp.data.user_name,
                        user_id: rsp.data.user_id,
                    });
                }
            });
        }
    },
    methods: {
    },

    data () {
        return {
        };
    },

    computed: {
        ...mapGetters([
            'is_login',
        ])
    }
}

</script>

