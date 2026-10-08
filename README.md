# 🦖 Aplikasi Eksplorasi Digimon

[![Kotlin](https://img.shields.io/badge/Kotlin-2.0.21-purple.svg?logo=kotlin)](https://kotlinlang.org/)
[![Jetpack Compose](https://img.shields.io/badge/Jetpack%20Compose-Material%203-blue.svg?logo=android)](https://developer.android.com/jetpack/compose)
[![Architecture](https://img.shields.io/badge/Architecture-MVVM-green.svg)](https://developer.android.com/topic/architecture)
[![API](https://img.shields.io/badge/API-Digi--API%20(DAPI)-orange.svg)](https://digi-api.com/)
[![Min SDK](https://img.shields.io/badge/Min%20SDK-30-lightgrey.svg)](https://developer.android.com/tools/releases/platforms)
[![Target SDK](https://img.shields.io/badge/Target%20SDK-37-blue.svg)](https://developer.android.com/tools/releases/platforms)

Aplikasi mobile berbasis Android modern untuk mencari, menjelajahi, dan melihat informasi detail berbagai Digimon. Proyek ini dibangun sebagai solusi teknis untuk **Responsi Praktikum Pemrograman Mobile (Paket D)** dengan menerapkan konsep arsitektur **MVVM**, **Jetpack Compose**, **Material Design 3**, **Custom Typography Serif**, **StateFlow UI State**, dan konsumsi REST API **Digi-API**.

---

## 📌 1. Latar Belakang & Permasalahan

Dunia digital sedang dilanda kekacauan akibat ulah seorang tamer jahat yang dapat mengendalikan Digimon sesuka hatinya. Untuk mengembalikan kedamaian dunia digital, kita harus menghadapi tamer tersebut dan pasukannya. Agar dapat menyusun strategi dan mengalahkan lawan, diperlukan informasi intelijen mengenai karakteristik setiap Digimon—termasuk **Nama**, **Level**, **Tipe**, dan **Atribut**.

Aplikasi ini hadir sebagai alat eksplorasi digital bagi para tamer untuk mengakses basis data Digimon secara *real-time* langsung dari server **Digi-API (DAPI)**.

---

## 📱 2. Screenshot Aplikasi

Dokumentasi visual antarmuka pengguna (*User Interface*) aplikasi:

| Home Screen (Grid List) | Detail Screen (Informasi Lengkap) 
| :---: | :---: | :---: |
| <img width="710" height="1601" alt="Home_Screen" src="https://github.com/user-attachments/assets/6e80a694-9c22-406e-85b4-c782b5e70973" />
 | <img width="710" height="1601" alt="Digimon_Detail" src="https://github.com/user-attachments/assets/625dfa15-3195-430a-8b26-9e0a034fa35f" />

| Katalog Digimon dalam format 2 kolom responsif | Detail lengkap: Level, Type, Atribut, dan Gambar |

---

## ⚙️ 3. Penjelasan Teknis Arsitektur & Komponen

Aplikasi ini dirancang dengan standar pengembangan Android modern (*Modern Android Development / MAD*) dan mematuhi seluruh spesifikasi teknis Paket D:

### A. Pemanfaatan Fitur Bahasa Kotlin
1. **Data Class**:
   - Merepresentasikan struktur data respon JSON API secara ringkas, *immutable*, dan *type-safe* tanpa boilerplate code:
     - [`DigimonListResponse`](app/src/main/java/com/example/aplikasieksplorasidigimon/data/Models.kt), [`DigimonListItem`](app/src/main/java/com/example/aplikasieksplorasidigimon/data/Models.kt), [`DigimonDetailResponse`](app/src/main/java/com/example/aplikasieksplorasidigimon/data/Models.kt)
     - Atribut bersarang (*nested DTO*): [`DigimonImage`](app/src/main/java/com/example/aplikasieksplorasidigimon/data/Models.kt), [`DigimonLevel`](app/src/main/java/com/example/aplikasieksplorasidigimon/data/Models.kt), [`DigimonType`](app/src/main/java/com/example/aplikasieksplorasidigimon/data/Models.kt), [`DigimonAttribute`](app/src/main/java/com/example/aplikasieksplorasidigimon/data/Models.kt)
     - State pembungkus data: `UiState.Success<T>(val data: T)`.
2. **Null Safety**:
   - Mencegah potensi `NullPointerException` (NPE) saat mem-parsing data API yang berpotensi `null` menggunakan *safe-call operator* (`?.`), *elvis operator* (`?:`), serta *smart casting*:
     ```kotlin
     // Pengambilan URL gambar pertama secara aman
     model = digimon.images?.firstOrNull()?.href

     // Penggabungan daftar level/tipe/atribut dengan fallback default jika kosong/null
     val levelText = digimon.levels?.takeIf { it.isNotEmpty() }?.joinToString { it.level } ?: "Unknown"
     val typeText = digimon.types?.takeIf { it.isNotEmpty() }?.joinToString { it.type } ?: "Unknown"
     val attrText = digimon.attributes?.takeIf { it.isNotEmpty() }?.joinToString { it.attribute } ?: "Unknown"
     ```
3. **Lambda Expressions & Higher-Order Functions**:
   - Menerapkan *State Hoisting* dan decoupling antar-Composable dengan melewatkan fungsi event sebagai parameter lambda:
     ```kotlin
     fun HomeScreen(viewModel: DigimonViewModel, onNavigateToDetail: (Int) -> Unit)
     fun DigimonItem(digimon: DigimonListItem, onClick: () -> Unit)
     ```
4. **Collection Operations**:
   - Penggunaan *functional operations* seperti `joinToString`, `takeIf`, `firstOrNull()`, dan mapping list item untuk mentransformasi koleksi data mentah dari API ke format teks yang siap ditampilkan di UI.

---

### B. User Interface (UI)
1. **100% Jetpack Compose**:
   - Seluruh tampilan dibangun secara deklaratif murni tanpa XML layout (`setContentView(R.layout...)` sepenuhnya ditiadakan).
2. **Material Design 3 (M3)**:
   - Menggunakan komponen resmi Material 3: `Scaffold`, `TopAppBar`, `Card`, `CardDefaults`, `Text`, `CircularProgressIndicator`, dan `Surface`.
3. **Custom Theme (`AplikasiEksplorasiDigimonTheme`)**:
   - Skema warna kustom bertema dunia digital petualangan dengan aksen oranye, biru, dan kuning:
     - `Orange40` (`#F57C00`), `Blue40` (`#1976D2`), `Yellow40` (`#FBC02D`) untuk Light Mode.
     - `Orange80` (`#FFB74D`), `Blue80` (`#64B5F6`), `Yellow80` (`#FFF176`) untuk Dark Mode.
   - Pada [`MainActivity.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/MainActivity.kt), disetel `dynamicColor = false` agar konsistensi identitas warna kustom aplikasi tetap terjaga di Android 12 ke atas tanpa tertimpa wallpaper *Material You*.
4. **Custom Typography**:
   - Sesuai instruksi penugasan, tipografi aplikasi diatur menggunakan jenis font **`FontFamily.Serif`** pada skala teks utama di [`Type.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/theme/Type.kt):
     - `bodyLarge`: Serif 16sp (Digimon card labels & item properties)
     - `headlineMedium`: Serif Bold 28sp (Detail Screen Digimon name)
     - `titleLarge`: Serif SemiBold 22sp (TopAppBar & header sections)

---

### C. Tampilan List & Data
- **`LazyVerticalGrid`**: Digunakan pada `HomeScreen` untuk menampilkan katalog Digimon dalam format 2 kolom adaptif (`GridCells.Fixed(2)`), memberikan efisiensi memori karena hanya me-render item yang terlihat di layar:
  ```kotlin
  LazyVerticalGrid(
      columns = GridCells.Fixed(2),
      contentPadding = PaddingValues(8.dp),
      modifier = Modifier.fillMaxSize()
  ) {
      items(digimons) { digimon ->
          DigimonItem(digimon = digimon, onClick = { onNavigateToDetail(digimon.id) })
      }
  }
  ```
- **`LazyColumn`**: Digunakan pada `DetailScreen` untuk menyusun informasi vertikal yang dapat di-scroll secara fleksibel di berbagai orientasi layar.

---

### D. Networking (Digi-API & Coil)
- **Base URL**: `https://digi-api.com/api/v1/`
- **HTTP Client**: **Retrofit 2** dipadukan dengan **GsonConverterFactory**.
- **Endpoint**:
  1. `GET digimon?pageSize=50` : Mengambil 50 daftar Digimon awal untuk katalog utama.
  2. `GET digimon/{id}` : Mengambil informasi detail lengkap Digimon spesifik berdasarkan ID.
- **Data Wajib yang Ditampilkan**:
  - ✅ **Nama Digimon** (`digimon.name`)
  - ✅ **Level** (`digimon.levels` misal: *Rookie*, *Champion*, *Ultimate*, *Mega*)
  - ✅ **Attribute** (`digimon.attributes` misal: *Vaccine*, *Data*, *Virus*, *Free*)
  - ✅ **Type** (`digimon.types` misal: *Reptile*, *Insect*, dll.)
  - ✅ **Gambar Digimon** (dimuat secara asinkron menggunakan library **Coil `AsyncImage`**).

---

### E. Arsitektur MVVM (Model - View - ViewModel - Repository)


1. **Model** ([`data/Models.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/data/Models.kt)): Struktur representasi data mentah dari respon JSON Digi-API.
2. **Repository** ([`data/DigimonRepository.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/data/DigimonRepository.kt)): Menjadi *Single Source of Truth* yang mengabstraksi pemanggilan API dari ViewModel menggunakan Kotlin Coroutines `suspend fun`.
3. **ViewModel** ([`ui/DigimonViewModel.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/DigimonViewModel.kt)): Mengelola state antarmuka yang tahan terhadap perubahan konfigurasi (*lifecycle-aware*). Mengubah data dari Repository menjadi `StateFlow<UiState>` yang dienkapsulasi (`MutableStateFlow` privat diekspos sebagai read-only `StateFlow`).
4. **View** ([`ui/HomeScreen.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/HomeScreen.kt), [`ui/DetailScreen.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/DetailScreen.kt)): UI deklaratif murni yang mengamati StateFlow melalui `collectAsState()` dan merender tampilan sesuai state saat itu.

---

### F. Navigation (Jetpack Navigation Compose)
Aplikasi memiliki alur navigasi maksimal 2 screen yang diatur dalam [`MainActivity.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/MainActivity.kt):
1. **Home Screen (`route = "home"`)**: Menampilkan katalog grid Digimon.
2. **Detail Screen (`route = "detail/{id}"`)**: Menerima argumen integer ID Digimon untuk memuat detail spesifik:
   ```kotlin
   NavHost(navController = navController, startDestination = "home") {
       composable("home") {
           HomeScreen(viewModel = viewModel, onNavigateToDetail = { id ->
               navController.navigate("detail/$id")
           })
       }
       composable(
           route = "detail/{id}",
           arguments = listOf(navArgument("id") { type = NavType.IntType })
       ) { backStackEntry ->
           val id = backStackEntry.arguments?.getInt("id") ?: return@composable
           DetailScreen(id = id, viewModel = viewModel, onNavigateBack = {
               navController.popBackStack()
           })
       }
   }
   ```

---

### G. UI State Management
Penerapan penanganan status antarmuka pengguna secara menyeluruh menggunakan generic sealed class di [`ui/UiState.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/UiState.kt):
```kotlin
sealed class UiState<out T> {
    object Loading : UiState<Nothing>()
    data class Success<out T>(val data: T) : UiState<T>()
    data class Error(val message: String) : UiState<Nothing>()
}
```
1. **`Loading`**: Menampilkan indikator berputar (`CircularProgressIndicator`) di tengah layar saat data sedang diunduh dari jaringan.
2. **`Success`**: Merender data konten Digimon ke dalam komponen Grid atau Detail.
3. **`Error`**: Menampilkan pesan kesalahan jika terjadi gangguan koneksi atau server API tidak merespon.

---

## 📂 4. Struktur Direktori Proyek

```
AplikasiEksplorasiDigimon/
├── app/
│   ├── src/
│   │   ├── main/
│   │   │   ├── java/com/example/aplikasieksplorasidigimon/
│   │   │   │   ├── data/
│   │   │   │   │   ├── DigimonApiService.kt    # Definisi Retrofit HTTP Endpoints (GET list, GET detail)
│   │   │   │   │   ├── DigimonRepository.kt    # Repository Pattern (suspend functions)
│   │   │   │   │   ├── Models.kt               # Kotlin Data Classes DTO
│   │   │   │   │   └── RetrofitClient.kt       # Singleton Retrofit Instance & Converter
│   │   │   │   ├── ui/
│   │   │   │   │   ├── theme/
│   │   │   │   │   │   ├── Color.kt            # Custom Digital World Color Palette
│   │   │   │   │   │   ├── Theme.kt            # Material 3 Theme Configuration
│   │   │   │   │   │   └── Type.kt             # Custom Typography FontFamily.Serif
│   │   │   │   │   ├── DetailScreen.kt         # Halaman Detail Digimon (LazyColumn)
│   │   │   │   │   ├── DigimonViewModel.kt     # ViewModel, Coroutines, & StateFlow
│   │   │   │   │   ├── HomeScreen.kt           # Halaman List Katalog Digimon (LazyVerticalGrid)
│   │   │   │   │   └── UiState.kt              # Sealed class UiState (Loading, Success, Error)
│   │   │   │   └── MainActivity.kt             # Entry point & NavHost Navigation Controller
│   │   │   └── AndroidManifest.xml             # Permission INTERNET & Activity Configuration
│   │   └── test/                               # Unit Testing
│   └── build.gradle.kts                        # Dependensi & Konfigurasi Modul Aplikasi
├── screenshots/                                # Dokumentasi Visual Aplikasi
│   ├── home_screen.png                         # Screenshot Halaman Katalog Digimon
│   ├── detail_screen.png                       # Screenshot Halaman Detail Digimon
│   ├── state_screen.png                        # Screenshot Loading & Error State
│   └── README.md                               # Panduan Folder Screenshot
├── build.gradle.kts                            # Konfigurasi Root Project
└── README.md                                   # Dokumentasi Teknis Utama Proyek
```

---

## 🚀 5. Cara Menjalankan Aplikasi

1. **Prasyarat**:
   - Android Studio (versi Ladybug / Koala / Hedgehog atau lebih baru).
   - Java Development Kit (JDK) 11 atau lebih baru.
   - Perangkat Android fisik atau Emulator Android dengan **Min SDK 30** (Android 11+).
   - Koneksi internet aktif (untuk mengambil data dari Digi-API).

2. **Langkah-langkah Instalasi**:
   - Clone repository ini:
     ```bash
     git clone https://github.com/ffakun221-wq/Responsi_PrakPemmob_PaketD.git
     ```
   - Buka project di Android Studio melalui menu **File > Open > Pilih folder `AplikasiEksplorasiDigimon`**.
   - Tunggu proses **Gradle Sync** hingga selesai.
   - Hubungkan perangkat Android fisik (aktifkan USB Debugging) atau jalankan Android Virtual Device (AVD).
   - Klik tombol **Run 'app'** (`Shift + F10`) pada toolbar Android Studio.

---

## 🎙️ 6. Panduan Video Penjelasan Kode (Outline Walkthrough)

Sesuai ketentuan **Poin 4.3** (*"Video penjelasan kode, bukan demo aplikasi"*), berikut adalah urutan materi yang disarankan saat merekam video penjelasan kode:

1. **Pengantar & Arsitektur (± 1 Menit)**:
   - Jelaskan pola arsitektur **MVVM** yang memisahkan View, ViewModel, Repository, dan Model.
2. **Data & Networking Layer (± 2 Menit)**:
   - Buka [`Models.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/data/Models.kt): jelaskan pemanfaatan **Data Class** dan **Null Safety**.
   - Buka [`DigimonApiService.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/data/DigimonApiService.kt) & [`RetrofitClient.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/data/RetrofitClient.kt): jelaskan endpoint Retrofit dan fungsi `suspend`.
   - Buka [`DigimonRepository.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/data/DigimonRepository.kt): jelaskan peran repository sebagai jembatan data.
3. **ViewModel & State Management (± 2 Menit)**:
   - Buka [`UiState.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/UiState.kt): jelaskan implementasi sealed class (`Loading`, `Success`, `Error`).
   - Buka [`DigimonViewModel.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/DigimonViewModel.kt): jelaskan eksekusi asynchronous via `viewModelScope.launch`, enkapsulasi `MutableStateFlow` ke `StateFlow`, dan pemanggilan data.
4. **UI Layer & Jetpack Compose (± 3 Menit)**:
   - Buka [`Theme.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/theme/Theme.kt) & [`Type.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/theme/Type.kt): jelaskan konfigurasi **Material 3 Custom Theme** dan **Custom Typography Serif**.
   - Buka [`HomeScreen.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/HomeScreen.kt): jelaskan observasi state menggunakan `collectAsState()`, percabangan UI (`when(state)`), dan penggunaan **`LazyVerticalGrid`**.
   - Buka [`DetailScreen.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/DetailScreen.kt): jelaskan `LaunchedEffect(id)`, **`LazyColumn`**, pemuatan gambar dengan **Coil `AsyncImage`**, serta rendering 4 data wajib (Nama, Level, Type, Attribute).
5. **Navigation (± 1 Menit)**:
   - Buka [`MainActivity.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/MainActivity.kt): jelaskan konfigurasi `NavHost`, 2 screen (Home dan Detail), dan pengiriman parameter ID antar halaman.

---

## 📋 7. Checklist Pemenuhan Kriteria Responsi

| Kriteria Penugasan | Status | Bukti / Keterangan Implementasi |
| :--- | :---: | :--- |
| **Kotlin Data Class** | ✅ Selesai | Model DTO di [`Models.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/data/Models.kt) & `UiState.Success` |
| **Kotlin Null Safety** | ✅ Selesai | Safe calls `?.`, Elvis `?:`, dan default fallbacks di [`DetailScreen.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/DetailScreen.kt) |
| **Kotlin Lambda & Collections** | ✅ Selesai | Trailing lambdas navigation & collection operations (`joinToString`, `takeIf`) |
| **Jetpack Compose (No XML)** | ✅ Selesai | 100% UI deklaratif Compose tanpa XML layout |
| **Material Design 3** | ✅ Selesai | Menggunakan komponen M3 (Scaffold, TopAppBar, Card, Surface) |
| **Custom Theme & Typography** | ✅ Selesai | Digital World palette di [`Theme.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/theme/Theme.kt) & `FontFamily.Serif` di [`Type.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/theme/Type.kt) |
| **List dengan LazyVerticalGrid** | ✅ Selesai | `LazyVerticalGrid(GridCells.Fixed(2))` di [`HomeScreen.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/HomeScreen.kt) |
| **Networking Digi-API (DAPI)** | ✅ Selesai | Retrofit 2 + Gson pada `https://digi-api.com/api/v1/` |
| **Minimal Data: Nama, Level, Attribute, Type** | ✅ Selesai | Ditampilkan lengkap dengan gambar Digimon (Coil) di [`DetailScreen.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/ui/DetailScreen.kt) |
| **Arsitektur MVVM (Model, View, ViewModel, Repo)** | ✅ Selesai | Pemisahan Model DTO, Repository, ViewModel, dan Composable View |
| **Maksimal 2 Screens dengan Navigation** | ✅ Selesai | Jetpack Navigation Compose: `home` dan `detail/{id}` di [`MainActivity.kt`](app/src/main/java/com/example/aplikasieksplorasidigimon/MainActivity.kt) |
| **State UI: Data, Loading, Error** | ✅ Selesai | Sealed class `UiState` dipadukan dengan `StateFlow` |
| **Ketentuan: Tanpa XML, DB, Auth, Lib Berlebih** | ✅ Selesai | Mematuhi seluruh larangan dan ketentuan teknis |
| **README.md Teknis & Screenshot** | ✅ Selesai | Berisi screenshot nyata dan penjelasan arsitektur lengkap |

---

## 🔗 8. Tautan Pengumpulan & Referensi

- **Repositori GitHub**: [https://github.com/ffakun221-wq/Responsi_PrakPemmob_PaketD.git](https://github.com/ffakun221-wq/Responsi_PrakPemmob_PaketD.git)

- **Dokumentasi Digi-API**: [https://digi-api.com/](https://digi-api.com/)
