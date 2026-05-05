
# PowerShell Rotating Star Display Script

function Show-RotatingStar {

    # Define star frames at different rotation angles
    $frames = @(
        @"












      * * * * *
     *       *
   *           *
  *             *
 *               *
"@,
        @"










   * * * * * *
  *           *
 * * * * * * * *
*                   *
 *           *
"@,
        @"












     *       *
   *           *
  *             *
 *               *
"@,
        @"










      * * * * *
    *           *
   *             *
  *               *
 *                 *
"@
    )
    
    $colors = @("Yellow", "Cyan", "Magenta", "Green")
    $duration = 10  # Rotate for 10 seconds
    $frameDelay = 0.2  # 200ms per frame
    $endTime = [DateTime]::Now.AddSeconds($duration)
    $frameIndex = 0
    

    Write-Host "`n⭐ Rotating Star Animation (Press Ctrl+C to stop)⭐`n" -ForegroundColor Magenta
    
    while ([DateTime]::Now -lt $endTime) {
        [Console]::Clear()
        Write-Host $frames[$frameIndex] -ForegroundColor $colors[$frameIndex]
        $frameIndex = ($frameIndex + 1) % $frames.Count
        Start-Sleep -Milliseconds ([int]($frameDelay * 1000))
    }
    
    [Console]::Clear()

    Write-Host "`n✨ Awesome! That was a rotating star display! ⭐`n" -ForegroundColor Magenta
}

# Display the rotating star
Show-RotatingStar