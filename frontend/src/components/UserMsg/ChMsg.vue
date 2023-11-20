<template>
    <div>
        <div class="header">
            个人信息
        </div>
        <div class="body">
            <el-form ref="form" :model="form" label-width="23%" id="selectForm" :rules="form_rules">

                <el-form-item label="ID：" prop="new_user_id">
                    <span>{{ form.new_user_id }}</span>
                    <!-- <el-input v-model="form.user_name"></el-input> -->
                </el-form-item>

                <el-form-item label="用户名：" prop="new_user_name">
                    <el-input v-model="form.new_user_name"  ></el-input>
                </el-form-item>

                <el-form-item label="真实姓名：" prop="new_real_name">
                    <el-input v-model="form.new_real_name"  ></el-input>
                </el-form-item>

                <el-form-item label="年龄：" prop="new_age">
                    <el-input v-model="form.new_age"  ></el-input>
                </el-form-item>

                <el-form-item label="性别：" prop="new_sex">
                    <el-input v-model="form.new_sex"  ></el-input>
                </el-form-item>
                <el-form-item label="电话：" prop="new_phone">
                    <el-input v-model="form.new_phone"  ></el-input>
                </el-form-item>

                <el-form-item label="邮箱：" prop="new_mail">
                    <el-input v-model="form.new_mail" ></el-input>
                </el-form-item>
                <el-form-item style="text-align:center;">
                    <el-button type="primary" @click="change()">确定</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
export default {
    created() {
        this.getdata()
    },
    data() {
        return {
            form: {
                new_user_id:'',
                new_real_name: '',
                new_sex: '',
                new_age: '',
                new_mail:'',
                new_phone:'',
                new_user_name:''
            },
            form_rules: {
                new_real_name: [{ required: true, message: "必填", trigger: 'blur' }],
                new_sex: [{ required: true, message: "必填", trigger: 'blur' }],
                new_age: [{ required: true, message: "必填", trigger: 'blur' }],
                new_user_name: [{ required: true, message: "必填", trigger: 'blur' }],
                new_mail: [{ required: true, message: "必填", trigger: 'blur' }],
                new_phone: [{ required: true, message: "必填", trigger: 'blur' }]
            }
        }
    },
    methods: {
        getdata(){
            this.$axios.get("/api/user/usertest").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.form.new_user_id=res.data.data.user_ID;
                }
            })
        },
        change() {
            this.$refs.form.validate(valid => {
                if (!valid)
                    return;
                else //验证通过再发送请求
                    {
                        this.$axios.post("/api/user/usermsg_chg", this.form).then((res) => {
                            if (res.data.status == 200) {
                                this.$message({
                                    message: res.data.msg,
                                    type: "success"
                                })
                            } else {
                                this.$message({
                                    message: res.data.msg,
                                    type: "error"
                                })
                            }
                        })
                    }
            })
        }

    },
}
</script>

<style scoped>
.header {
    width: 100%;
    height: 10%;
    text-align: center;
    line-height: 64px;
    font-size: 20px;
    font-weight: 800;
    border-bottom: 1px solid #e3e3e3;
}

.body {
    width: 40%;
    /* margin: auto; */
    margin-top: 30px;
    margin-left: 30px;

}

#selectForm>>>.el-form-item__label {
    font-size: 18px;
}

span {
    font-size: 18px;
}
</style>