package com.example.aplikasieksplorasidigimon.data

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object RetrofitClient {
    private const val BASE_URL = "https://digi-api.com/api/v1/"

    val apiService: DigimonApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(DigimonApiService::class.java)
    }
}
