package com.example.aplikasieksplorasidigimon.ui

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.aplikasieksplorasidigimon.data.DigimonDetailResponse
import com.example.aplikasieksplorasidigimon.data.DigimonListItem
import com.example.aplikasieksplorasidigimon.data.DigimonRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch

class DigimonViewModel(private val repository: DigimonRepository = DigimonRepository()) : ViewModel() {

    private val _listState = MutableStateFlow<UiState<List<DigimonListItem>>>(UiState.Loading)
    val listState: StateFlow<UiState<List<DigimonListItem>>> = _listState.asStateFlow()

    private val _detailState = MutableStateFlow<UiState<DigimonDetailResponse>>(UiState.Loading)
    val detailState: StateFlow<UiState<DigimonDetailResponse>> = _detailState.asStateFlow()

    init {
        fetchDigimonList()
    }

    private fun fetchDigimonList() {
        viewModelScope.launch {
            _listState.value = UiState.Loading
            try {
                val response = repository.getDigimonList()
                _listState.value = UiState.Success(response.content)
            } catch (e: Exception) {
                _listState.value = UiState.Error(e.message ?: "Unknown Error")
            }
        }
    }

    fun fetchDigimonDetail(id: Int) {
        viewModelScope.launch {
            _detailState.value = UiState.Loading
            try {
                val response = repository.getDigimonDetail(id)
                _detailState.value = UiState.Success(response)
            } catch (e: Exception) {
                _detailState.value = UiState.Error(e.message ?: "Unknown Error")
            }
        }
    }
}
