<template>
    <div>
        <div class="header">
            食品信息
        </div>
        <div class="body">
            <el-table :data="tableData" style="width: 100%" class="table">
                <el-table-column prop="food" label="人气产品" width="325" align="center">
                </el-table-column>
                
                <el-table-column prop="sale" label="销量" width="325" align="center">
                </el-table-column>
                <el-table-column prop="food1" label="好吃不贵" width="325" align="center">
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
            this.$axios.get("/api/manager/food").then((res) => {
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