/**
 * nim_nip_toggle.js
 * Menyembunyikan field NIM atau NIP secara otomatis di Django Admin
 * berdasarkan role yang dipilih (dosen = tampilkan NIP, mahasiswa = tampilkan NIM).
 */
(function () {
    'use strict';

    function toggleNimNip() {
        var roleSelect = document.getElementById('id_role');
        if (!roleSelect) return;

        var nimRow = document.querySelector('.field-nim');
        var nipRow = document.querySelector('.field-nip');
        var kelasRow = document.querySelector('.field-kelas');

        if (!nimRow || !nipRow) return;

        var role = roleSelect.value;

        if (role === 'dosen') {
            // Tampilkan NIP, sembunyikan NIM dan Kelas
            nipRow.style.display = '';
            nimRow.style.display = 'none';
            if (kelasRow) kelasRow.style.display = 'none';
        } else {
            // Tampilkan NIM dan Kelas, sembunyikan NIP
            nimRow.style.display = '';
            nipRow.style.display = 'none';
            if (kelasRow) kelasRow.style.display = '';
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        var roleSelect = document.getElementById('id_role');
        if (roleSelect) {
            // Jalankan saat halaman pertama kali dimuat
            toggleNimNip();
            // Jalankan setiap kali dropdown role berubah
            roleSelect.addEventListener('change', toggleNimNip);
        }
    });
})();
