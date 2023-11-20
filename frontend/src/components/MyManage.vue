<template>
    <div>
        <div class="header">
            &nbsp;&nbsp; 学苑五楼---管理员
        </div>
        <div class="body">
            <div class="liner">
                <el-menu default-active="1" class="el-menu-vertical-demo" background-color="#545c64" text-color="#fff"
                    active-text-color="#ffd04b" @select="handleselect">

                    <el-menu-item index="1">
                        <i class="el-icon-s-shop"></i>
                        <span slot="title">店铺管理</span>
                    </el-menu-item>

                    <el-menu-item index="2">
                        <i class="el-icon-s-custom"></i>
                        <span slot="title">服务员管理</span>
                    </el-menu-item>

                    <el-menu-item index="3">
                        <i class="el-icon-s-check"></i>
                        <span slot="title">送餐员管理</span>
                    </el-menu-item>


                    <el-menu-item index="4">
                        <i class="el-icon-s-check"></i>
                        <span slot="title">派送信息</span>
                    </el-menu-item>

                    <el-submenu index="100">
                        <template slot="title">
                            <i class="el-icon-s-order"></i>
                            <span>订单管理</span>
                        </template>
                        <el-menu-item-group>

                            <!-- <el-menu-item index="9">订单概览</el-menu-item> -->
                            <el-menu-item index="10">产品信息</el-menu-item>
                            <el-menu-item index="6">大额订单</el-menu-item>
                            <el-menu-item index="7">小额订单</el-menu-item>
                            <el-menu-item index="8">未发货订单</el-menu-item>
                        </el-menu-item-group>

                    </el-submenu>

                </el-menu>
            </div>
            <div class="main">
                <div id="manageshop" v-show="active == 1">
                    <manageshop></manageshop>
                </div>

                <div id="manageserver" v-show="active == 2">
                    <manageserver></manageserver>
                </div>

                <div id="managedispatcher" v-show="active == 3">
                    <managedispatcher></managedispatcher>
                </div>


                <div id="wuliuunended" v-show="active == 4">
                    <wuliuunended></wuliuunended>
                </div>

                
                <div id="ordersended" v-show="active == 6">
                    <ordersended></ordersended>
                </div>
                <div id="ordersending" v-show="active == 7">
                    <ordersending></ordersending>
                </div>

                <div id="orderunsend" v-show="active == 8">
                    <orderunsend></orderunsend>
                </div>

                <!-- <div id="OrderWay" v-show="active == 9">
                    <OrderWay></OrderWay>
                </div> -->
                <div id="FoodRank" v-show="active == 10">
                    <FoodRank></FoodRank>>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import manageshop from '@/components/ManageShop.vue'
import manageserver from '@/components/ManageServer.vue'
import managedispatcher from '@/components/ManageDispatcher.vue'

import wuliuunended from '@/components/ManageWuliu/WuliuUnended.vue'
import ordersended from '@/components/ManageOrder/BeSended.vue'
import ordersending from '@/components/ManageOrder/BeSending.vue'
import orderunsend from '@/components/ManageOrder/UnSend.vue'
// import OrderWay from '@/components/ManageOrder/OrderWay.vue'
import FoodRank from '@/components/ManageOrder/FoodRank.vue'
export default {
    components: {
    manageshop: manageshop,
    manageserver: manageserver,
    managedispatcher: managedispatcher,
    
    wuliuunended: wuliuunended,
    ordersended: ordersended,
    ordersending: ordersending,
    orderunsend: orderunsend,
    // OrderWay: OrderWay,
    FoodRank: FoodRank
},
    data() {
        return {
            active: 1,
        }
    },
    methods: {
        handleselect(index) {
            this.active = index;
        }
    },
}
</script>

<style scoped>
.header {
    width: 100%;
    height: 10vh;
    /* text-align: center; */
    line-height: 10vh;
    font-size: 25px;
    font-weight: 800;
    background-color: #e3e3e3;
    /* padding-left: 100px; */
}

.body {
    width: 100%;
    height: 648px;
    display: flex;
    justify-content: space-around;
}

.liner {
    width: 15%;
    height: 100%;
    background-color: #545c64;
}

.main {
    width: 85%;
}
</style>