package com.example.aplikasieksplorasidigimon.data

import retrofit2.http.GET
import retrofit2.http.Path

interface DigimonApiService {
    @GET("digimon?pageSize=50")
    suspend fun getDigimonList(): DigimonListResponse

    @GET("digimon/{id}")
    suspend fun getDigimonDetail(@Path("id") id: Int): DigimonDetailResponse
}
