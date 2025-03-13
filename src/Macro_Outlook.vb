
' En ThisOutlookSession
Dim WithEvents objReminders As Outlook.Reminders
Private Const HoraInicio As Integer = 8 ' Hora de inicio (8 a.m.)
Private Const HoraFin As Integer = 17 ' Hora de fin (5 p.m.)

Private Sub Application_Startup()
    Set objReminders = Application.Reminders
    ProgramarRecordatorios
End Sub

Private Sub objReminders_ReminderFire(ByVal ReminderObject As Reminder)
    If ReminderObject.Item.Subject = "EjecutarMacroExportarCorreos" Then
        ExportarCorreosAMSG_Y_LimpiarBandeja11
        ReminderObject.Item.Delete ' Elimina el recordatorio antiguo
        ProgramarRecordatorios ' Programa el siguiente
    End If
End Sub

Sub ProgramarRecordatorios()
    Dim objAppointment As Outlook.AppointmentItem
    Dim hora As Integer
    Dim ahora As Date

    ahora = Now

    For hora = HoraInicio To HoraFin - 1 ' Recorre las horas desde la hora de inicio hasta la hora de fin - 1
        Set objAppointment = Application.CreateItem(olAppointmentItem)
        With objAppointment
            .Subject = "EjecutarMacroExportarCorreos"
            .Start = DateAdd("h", hora, DateValue(ahora)) + TimeValue("00:20:00") ' Configura la hora y el minuto
            .ReminderMinutesBeforeStart = 0
            .ReminderSet = False
            .Save
        End With
    Next hora
End Sub