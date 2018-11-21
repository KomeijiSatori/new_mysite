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

