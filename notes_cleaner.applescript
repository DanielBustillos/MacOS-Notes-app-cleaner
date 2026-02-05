tell application "Notes"
    
    set sourceName to system attribute "SOURCE_FOLDER"
    set targetName to system attribute "TARGET_FOLDER"
    set workerPath to system attribute "GEMINI_WORKER_PATH"
    set promptPath to system attribute "GEMINI_PROMPT_PATH"
    set apiKey to system attribute "GOOGLE_API_KEY"
    set geminiModel to system attribute "GEMINI_MODEL"
    
    try
        set sourceFolder to folder sourceName
    on error
        return
    end try
    
    if not (exists folder targetName) then
        make new folder with properties {name:targetName}
    end if
    set targetFolder to folder targetName
    
    set noteList to notes of sourceFolder
    set totalNotes to count of noteList
    set index to 0
    
    do shell script "echo 'Scanning " & totalNotes & " notes...' > /dev/tty"
    
    repeat with aNote in noteList
        set index to index + 1
        
        set noteTitle to name of aNote
        set noteBody to plaintext of aNote
        set attachmentCount to count of attachments of aNote
        
        -- Note creation date (YYYY-MM-DD) for Gemini
        set cd to creation date of aNote
        set y to year of cd
        set m to (month of cd) as integer
        set d to day of cd
        set mStr to text -2 thru -1 of ("00" & (m as text))
        set dStr to text -2 thru -1 of ("00" & (d as text))
        set noteDateStr to (y as text) & "-" & mStr & "-" & dStr
        
        -- Visual snippet
        set snippet to ""
        if length of noteBody > 50 then
            set snippet to text 1 thru 50 of noteBody
        else
            set snippet to noteBody
        end if
        set snippetClean to do shell script "echo " & quoted form of snippet & " | tr -d '\n' | tr -d '\r'"
        
        set decision to "PENDING"
        set reason to ""
        
        -- Local filter: only protect if it has REAL attachments > 0
        if attachmentCount > 0 then
            set decision to "KEEP"
            set reason to "[Attachments]"
        else
            -- Query Gemini
            try
                set respAI to do shell script "export GEMINI_PROMPT_PATH=" & quoted form of promptPath & " GOOGLE_API_KEY=" & quoted form of apiKey & " GEMINI_MODEL=" & quoted form of geminiModel & " NOTE_DATE=" & quoted form of noteDateStr & "; echo " & quoted form of noteBody & " | python3 " & quoted form of workerPath & " 2>&1"
                -- If the worker returned ERROR: on the first line, show it
                if respAI starts with "ERROR:" then
                    set errLine to paragraph 1 of respAI
                    do shell script "echo " & quoted form of ("Error: " & errLine) & " > /dev/tty"
                    set decision to "MOVE"
                    set reason to "[Error]"
                else if respAI contains "MOVE" then
                    set decision to "MOVE"
                    set reason to "[AI: Junk/Link]"
                else
                    set decision to "KEEP"
                    set reason to "[AI: Keep]"
                end if
            on error errMsg
                -- If do shell script fails (worker crashed, etc.): do not keep, print error
                do shell script "echo " & quoted form of ("Process error: " & errMsg) & " > /dev/tty"
                set decision to "MOVE"
                set reason to "[Error]"
            end try
        end if
        
        -- Action
        if decision is "MOVE" then
            move aNote to targetFolder
            do shell script "echo '[" & index & "/" & totalNotes & "] MOVE   | " & noteTitle & " | (" & snippetClean & "...)' > /dev/tty"
        else
             do shell script "echo '[" & index & "/" & totalNotes & "] KEEP | " & noteTitle & " | " & reason & "' > /dev/tty"
        end if
        
        delay 4
        
    end repeat
    
    do shell script "echo 'Done.' > /dev/tty"
end tell
