<script>
    const table_data = {{ table_data|tojson }}
    chartLib.makeChart(table_data)
</script>