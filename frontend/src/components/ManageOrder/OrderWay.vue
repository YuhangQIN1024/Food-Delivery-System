<template>
    <div>
        <div class="header">
            订单概览
        </div>
        <div class="body">
            <el-table :data="tableData" style="width: 100%" class="table">
                <el-table-column prop="orderway_name" label="下单方式" width="500" align="center">
                </el-table-column>
                <el-table-column prop="count" label="数量" width="500" align="center">
                </el-table-column>
            </el-table>


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
            tableData: [],
        }
    },
    methods: {
        getdata() {
            this.$axios.get("/api/manager/howorder").then((res) => {
                console.log(res.data);
                if (res.data.status == 200) {
                    this.tableData = res.data.tabledata;
                }
            })
        }
    }

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

    width: 76%;
    margin: auto;
    margin-top: 30px;
}
</style>