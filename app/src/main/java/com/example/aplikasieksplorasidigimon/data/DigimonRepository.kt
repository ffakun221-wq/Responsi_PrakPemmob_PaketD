package com.example.aplikasieksplorasidigimon.data

class DigimonRepository(private val apiService: DigimonApiService = RetrofitClient.apiService) {

    suspend fun getDigimonList(): DigimonListResponse {
        return apiService.getDigimonList()
    }

    suspend fun getDigimonDetail(id: Int): DigimonDetailResponse {
        return apiService.getDigimonDetail(id)
    }
}
