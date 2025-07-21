# Kontrollera att filen existerar innan k�rning
$AppPath = "C:\Users\mahoo\ai_juridik_lokal\juridisk_ai_app"
$ScriptFile = "streamlit_app.py"
$FullPath = Join-Path $AppPath $ScriptFile

if (Test-Path $FullPath) {
    Write-Host "? Startar juridisk AI-app fr�n $FullPath ..."
    Set-Location $AppPath
    streamlit run $ScriptFile
} else {
    Write-Error "? Hittar inte: $FullPath"
}
