package com.example.aplikasieksplorasidigimon.data

data class DigimonListResponse(
    val content: List<DigimonListItem>
)

data class DigimonListItem(
    val id: Int,
    val name: String,
    val image: String
)

data class DigimonDetailResponse(
    val id: Int,
    val name: String,
    val images: List<DigimonImage>?,
    val levels: List<DigimonLevel>?,
    val types: List<DigimonType>?,
    val attributes: List<DigimonAttribute>?
)

data class DigimonImage(
    val href: String
)

data class DigimonLevel(
    val level: String
)

data class DigimonType(
    val type: String
)

data class DigimonAttribute(
    val attribute: String
)
