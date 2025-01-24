from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from psutil import (
    sensors_battery,
    virtual_memory,
    swap_memory,
    cpu_percent,
    sensors_temperatures,
    disk_io_counters,
    disk_partitions,
    disk_usage,
    net_io_counters,
    net_if_addrs,
    boot_time,
    users,
    pids,
    process_iter,
)
from datetime import datetime
from time import sleep

def bytes_to_gb(value):
    return value / 1024 / 1024 / 1024

console = Console()

while True:
    try:

        p_list = []
        for proc in process_iter(attrs=None, ad_value=None):
            proc_info = proc.as_dict(attrs=["name", "cpu_percent"])
            if proc_info["cpu_percent"] > 0:
                p_list.append(proc_info)

        ordenados = sorted(
            p_list, key=lambda p: p["cpu_percent"], reverse=True
        )[:10]

        process_table = Table(title="Processos (TOP 10 por CPU)", title_style="bold blue")
        process_table.add_column("Nome", style="cyan", justify="left")
        process_table.add_column("CPU (%)", style="magenta", justify="right")
        for proc in ordenados:
            process_table.add_row(proc["name"], f"{proc['cpu_percent']}")

        mem_panel = Panel(
            f"[cyan]RAM: {virtual_memory().percent}%[/cyan]\n"
            f"[magenta]SWAP: {swap_memory().percent}%[/magenta]",
            title="Memória",
            border_style="green",
        )

        cpu_usage = cpu_percent()
        cpu_panel = Panel(
            f"[yellow]Uso total: {cpu_usage}%[/yellow]\n",
            title="CPU",
            border_style="red",
        )

        temperatures = sensors_temperatures()
        cpu_temp = temperatures.get("coretemp", [{}])[0].get("current", 0)
        pch_temp = temperatures.get("pch_skylake", [{}])[0].get("current", 0)

        cpu_panel.renderable += (
            f"[bold white]Temperatura CPU: {cpu_temp}°C\n"
            f"Temperatura PCH: {pch_temp}°C[/bold white]"
        )

        disk_table = Table(title="Disco", title_style="bold blue")
        disk_table.add_column("Partição", style="cyan", justify="left")
        disk_table.add_column("Uso (%)", style="magenta", justify="right")
        disk_table.add_column("Lido (GB)", style="green", justify="right")
        disk_table.add_column("Escrito (GB)", style="yellow", justify="right")

        partitions = disk_partitions()
        counters = disk_io_counters(perdisk=True)
        for partition in partitions:
            partition_name_counter = partition.device.split("/")[-1]
            disk_bytes = counters.get(partition_name_counter, None)
            if disk_bytes:
                disk_table.add_row(
                    partition.mountpoint,
                    f"{disk_usage(partition.mountpoint).percent}",
                    f"{bytes_to_gb(disk_bytes.read_bytes):.2f}",
                    f"{bytes_to_gb(disk_bytes.write_bytes):.2f}",
                )

        net_counters = net_io_counters()
        addrs = net_if_addrs()
        ipv4 = addrs.get("wlp2s0", [{}])[0].get("address", "N/A")
        net_panel = Panel(
            f"[cyan]IPv4: {ipv4}[/cyan]\n"
            f"[green]Enviado: {bytes_to_gb(net_counters.bytes_sent):.2f} GB[/green]\n"
            f"[magenta]Recebido: {bytes_to_gb(net_counters.bytes_recv):.2f} GB[/magenta]",
            title="Rede",
            border_style="blue",
        )

        battery = sensors_battery().percent if sensors_battery() else "N/A"
        user = users()[0].name if users() else "N/A"
        boot = datetime.fromtimestamp(boot_time()).strftime("%Y-%m-%d %H:%M:%S")
        info_panel = Panel(
            f"[white]Bateria: {battery}%[/white]\n"
            f"[cyan]Usuário: {user}[/cyan]\n"
            f"[green]Horário do Boot: {boot}[/green]\n"
            f"[magenta]Processos ativos: {len(pids())}[/magenta]",
            title="Outros",
            border_style="yellow",
        )

        console.clear()
        console.print(process_table)
        console.print(mem_panel)
        console.print(cpu_panel)
        console.print(disk_table)
        console.print(net_panel)
        console.print(info_panel)

        sleep(0.5)
    except KeyboardInterrupt:
        console.print("[red]Monitoramento encerrado![/red]")
        break
