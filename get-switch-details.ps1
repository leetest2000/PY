# Script to gather Show interface from switches and export to csv file
$todayDate = Get-Date -Format "yyMMdd"
# Set ouput files
$file = "d:\scripts\get-detailed-switch-info\output\Switch_info-$($todayDate).csv"
$file1 = "d:\scripts\get-detailed-switch-info\output\cdp\CDP_Switch_info-$($todayDate).csv"
# Set input files
$sshfile = "d:\scripts\get-detailed-switch-info\sshlist.csv"
$telnetfile = "d:\scripts\get-detailed-switch-info\telnetlist.csv"
# Write headers to output files
$headers = "Site,Switch_Name,IP_Address,Hostname,Interface,Hardware_type,Link_status,Description,Interface_ip,Last_input,Last_output,Uptime_years,Uptime_weeks,Uptime_days" 
$headers | Out-File $file -append
$cdpheader = "Site,Switch_Name,IP_Address,Local_Interface,CDP_Neighbor,Neighbor_Platform,Neighbor_Interface"
$cdpheader | Out-File $file1

# Import switch details from ssh CSV & Run Script
Import-Csv $sshfile | ForEach {
    Write-Host "Processing switch $($_.Name), IP address $($_.IP_Address)"
    py d:\scripts\get-detailed-switch-info\showInterface-ssh.py $_.IP_Address $_.Site $_.Name | Out-File $file -append
    py d:\scripts\get-detailed-switch-info\showcdpneig-ssh.py $_.IP_Address $_.Site $_.Name | Out-File $file1 -append
}

# Import switch details from telnet CSV & Run Script
Import-Csv $telnetfile | ForEach {
    Write-Host "Processing switch $($_.Name), IP address $($_.IP_Address)"
    py d:\scripts\get-detailed-switch-info\showInterface-telnet.py $_.IP_Address $_.Site $_.Name | Out-File $file -append
    py d:\scripts\get-detailed-switch-info\showcdpneig-telnet.py $_.IP_Address $_.Site $_.Name | Out-File $file1 -append
}
