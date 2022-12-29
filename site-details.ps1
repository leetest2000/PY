# Script to gather Show interface from switches and export to csv file
$todayDate = Get-Date -Format "yyMMdd"
$folder= "D:\Scripts\Get-detailed-switch-info\SiteDetails\"
$file = "D:\Scripts\Get-detailed-switch-info\SiteDetails\Site_info-$($todayDate).txt"
$sshfile = "D:\Scripts\Get-detailed-switch-info\sshlist.csv"

# Import switch details from ssh CSV & Run Script
Import-Csv $sshfile | ForEach {
 if (Test-path D:\Scripts\Get-detailed-switch-info\SiteDetails\$($_.Site)-site) {
  Write-Host "Folder Exists"
 }
 else{
  md D:\Scripts\Get-detailed-switch-info\SiteDetails\$($_.Site)-site
  Write-Host "Folder Created"
  }
 $file = "D:\Scripts\Get-detailed-switch-info\SiteDetails\$($_.Site)-site\Site-$($_.Site)-$($todayDate).txt"
 Write-Output $_.Name
 $interfaces = py D:\Scripts\Get-detailed-switch-info\SiteDetails\site_information-ssh.py $_.IP_Address $_.Site $_.Name
 $interfaces | Out-File $file -append
}
