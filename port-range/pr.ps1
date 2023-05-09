param(
    [Parameter(Mandatory=$true, Position=0)]
    [int]$StartPort,
    [Parameter(Position=1)]
    [int]$EndPort = $StartPort
)

$results = @()

# TCP connections
Get-NetTCPConnection | Where-Object { $_.LocalPort -ge $StartPort -and $_.LocalPort -le $EndPort } | ForEach-Object {
    $ProcessId = $_.OwningProcess
    $ConnectionState = $_.State
    $LocalPort = $_.LocalPort
    $Protocol = 'TCP'
    $Process = Get-Process | Where-Object { $_.Id -eq $ProcessId }
    $results += New-Object PSObject -Property @{
        Id = $Process.Id
        ProcessName = $Process.ProcessName
        Path = $Process.Path
        State = $ConnectionState
        LocalPort = $LocalPort
        Protocol = $Protocol
    }
}

# UDP connections
Get-NetUDPEndpoint | Where-Object { $_.LocalPort -ge $StartPort -and $_.LocalPort -le $EndPort } | ForEach-Object {
    $ProcessId = $_.OwningProcess
    $LocalPort = $_.LocalPort
    $Protocol = 'UDP'
    $Process = Get-Process | Where-Object { $_.Id -eq $ProcessId }
    $results += New-Object PSObject -Property @{
        Id = $Process.Id
        ProcessName = $Process.ProcessName
        Path = $Process.Path
        LocalPort = $LocalPort
        Protocol = $Protocol
    }
}

$results | Format-Table Protocol, LocalPort, ProcessName, Id, Path, State
