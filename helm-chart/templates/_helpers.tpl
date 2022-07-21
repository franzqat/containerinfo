{{- define "common.labels.standard" -}}
app.kubernetes.io/name: {{ .Release.Name }}
helm.sh/chart: {{ .Chart.Name }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}