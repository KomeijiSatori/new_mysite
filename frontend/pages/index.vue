<template>
    <div>
        <Card style="width:350px" v-show="!is_login">
            <p slot="title">
                <Icon type="ios-person"/>
                Log In
            </p>
            <Form ref="login_form" :model="login_form" :rules="ruleValidate" :label-width="80">
                <FormItem label="user name" prop="name">
                    <Input v-model="login_form.name" label="用户名" placeholder="Input user name"></Input>
                </FormItem>
                <FormItem label="password" prop="password">
                    <Input type="password" v-model="login_form.password" placeholder="Input password" ></Input>
                </FormItem>
                <FormItem>
                    <Button type="primary" @click="handleLogin()">submit</Button>
                    <Button type="default" @click="handleReset()" style="margin-left: 8px">reset</Button>
                </FormItem>
            </Form>
        </Card>
        <Card style="width:350px" v-show="is_login">
            <p slot="title">
                <Icon type="ios-exit-outline"/>
                Logout
            </p>
            <Button slot="extra" type="primary" @click="handleLogout()" style="margin-left: 8px">log out</Button>
            <p>Hello, {{ user_info.user_name }}. Your ID is {{ user_info.user_id }}</p>
        </Card>
    </div>
</template>

<script>
import { mapState, mapGetters } from 'vuex';
import UserClient from '@/api/user_client';

export default {
    async asyncData ({ app }) {

    },
    methods: {
        handleLogin () {
            this.$refs['login_form'].validate((valid) => {
                if (valid) {
                    let payloads = {
                        user_name: this.login_form.name,
                        user_password: this.login_form.password,
                    }
                    UserClient.login(payloads).then(rsp => {
                        if (rsp.code != 0) {
                            this.$Message.warning(rsp.message);
                        } else {
                            this.$store.commit("login", {
                                user_name: rsp.data.user_name,
                                user_id: rsp.data.user_id,
                            });
                            this.$Message.success(rsp.message);
                        }
                    });
                } else {
                    this.$Message.error('invalid form!');
                }
            })
        },
        handleReset () {
            this.$refs['login_form'].resetFields();
        },
        handleLogout () {
            UserClient.logout().then(rsp => {
                if (rsp.code != 0) {
                    this.$Message.warning(rsp.message);
                } else {
                    this.$store.commit("logout");
                    this.$Message.success(rsp.message);
                }
            });
        }
    },

    data () {
        return {
            login_form: {
                name: "",
                password: "",
            },
            ruleValidate: {
                name: [
                    { required: true, message: 'user name cannot be empty', trigger: 'blur', }
                ],
                password: [
                    { required: true, message: 'password cannot be empty', trigger: 'blur', }
                ]
            },
        };
    },

    computed: {
        ...mapState([
            'user_info',
        ]),
        ...mapGetters([
            'is_login',
        ])
    }
}

</script>
