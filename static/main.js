function warning(text, callback) {
    layer.open({
        type: 1,
        title: false,
        closeBtn: false,
        area: '500px;',
        shade: 0.8,
        id: 'warning',
        btn: ['确定', '取消'],
        btnAlign: 'c',
        moveType: 1,
        content: '<div style="padding: 50px; line-height: 22px; background-color: #EE2C2C; color: #fff; font-weight: 300;">' + text + '</div>',
        yes: function (index) {
            callback()
            layer.close(index)
        }
    })
}

function startWebsiteStressTest() {
    $("#bashCommand").val("ab -c " + $("#concurrentNumber").val() + " -n " + $("#numberOfRequests").val() + " " + $("#stressTestURL").val())
    executeCommand("websiteStressTest")
}

function getDiskInfo() {
    requestPlugin("getDisksInfo", {
    }, function (rdata) {
    })
}

function mountNewDisk(disk) {
    layer.open({
        title: '挂载硬盘',
        area: ['800px', '350px'],
        content: $("#mount-disk-dialog").html().replaceAll("template-", "").replaceAll("sdb", disk),
        btn1: function (index) {
            disk = $("#disk-1").val()
            filesystem = $("#filesystem-1").val()
            mountPoint = $("#mount-point-1").val()
            options = $("#options-1").val()
            warning("注意！此操作可能导致数据丢失！！<br><br>本次操作将会在硬盘[" + disk + "]上创建一个分区，并使用[" + filesystem + "]文件系统格式化此分区，最后挂载到挂载点[" + mountPoint + "]<br><br>本功能仅可在未分区硬盘中使用，否则可能导致意外的问题！<br>请勿将磁盘挂载到一些存在重要系统文件的目录，比如/、/bin、/etc等，如果挂载，将导致系统异常或数据丢失！<br>本工具暂时不支持迁移www目录功能，如果将磁盘直接挂载到/www，将会导致宝塔面板以及网站出现异常！<br><br>是否继续操作？", function () {
                requestPlugin("mountNewDisk", {
                    disk: disk,
                    filesystem: filesystem,
                    mountPoint: mountPoint,
                    options: options
                }, function (rdata) {
                    getDiskInfo()
                    layer.msg(rdata.msg, {
                        icon: rdata.status ? 1 : 2
                    })
                })
            })
            layer.close(index)
        }
    })
}

function umountPartition(partition) {
    warning("注意！此操作可能导致数据丢失！！<br><br>本次操作将卸载分区[" + partition + "]<br><br>被卸载的磁盘不会被格式化，重新挂载后数据仍然存在<br>如需重新挂载，请使用“手动挂载分区”功能挂载！<br><br>是否继续操作？", function () {
        requestPlugin("umountPartition", {
            partition: partition
        }, function (rdata) {
            getDiskInfo()
            layer.msg(rdata.msg, {
                icon: rdata.status ? 1 : 2
            })
        })
    })
}

function formatPartition(partition, mountPoint) {
    if (mountPoint == "") {
        mountPoint = "/kagamine"
    }
    layer.open({
        title: '格式化分区',
        area: ['800px', '350px'],
        content: $("#mount-disk-dialog").html().replaceAll("template-", "").replaceAll("磁盘地址", "分区地址").replaceAll("sdb", partition).replaceAll("/kagamine", mountPoint),
        btn1: function (index) {
            partition = $("#disk-1").val()
            filesystem = $("#filesystem-1").val()
            mountPoint = $("#mount-point-1").val()
            options = $("#options-1").val()
            warning("注意！您正在格式化分区！！<br><br>本次操作将格式化分区[" + partition + "]！<br><br>进行此操作后，此分区的数据将被全部清空！<br>如果您不小心格式化了存放有重要数据的磁盘，请立即停止写入并关闭服务器，然后联系专业数据恢复公司！<br><br>是否继续操作？", function () {
                requestPlugin("formatPartition", {
                    partition: partition,
                    mountPoint: mountPoint,
                    filesystem: filesystem
                }, function (rdata) {
                    getDiskInfo()
                    layer.msg(rdata.msg, {
                        icon: rdata.status ? 1 : 2
                    })
                })
            })
            layer.close(index)
        }
    })

}

function mountPartition(partition, fstype) {
    layer.open({
        title: '挂载分区',
        area: ['800px', '350px'],
        content: $("#mount-disk-dialog").html().replaceAll("template-", "").replaceAll("磁盘地址", "分区地址").replaceAll("ext4", fstype).replaceAll("sdb", partition),
        btn1: function (index) {
            partition = $("#disk-1").val()
            filesystem = $("#filesystem-1").val()
            mountPoint = $("#mount-point-1").val()
            options = $("#options-1").val()
            warning("注意！此操作可能导致数据丢失！！<br><br>本次操作将挂载分区[" + partition + "]<br><br>请确认您输入的文件系统是否正确，否则将挂载失败！<br>请勿将磁盘挂载到一些存在重要系统文件的目录，比如/、/bin、/etc等，如果挂载，将导致系统异常或数据丢失！<br>本工具暂时不支持迁移www目录功能，如果将磁盘直接挂载到/www，将会导致宝塔面板以及网站出现异常！<br><br>是否继续操作？", function () {
                requestPlugin("mountPartition", {
                    partition: partition,
                    filesystem: filesystem,
                    mountPoint: mountPoint,
                    options: options
                }, function (rdata) {
                    getDiskInfo()
                    layer.msg(rdata.msg, {
                        icon: rdata.status ? 1 : 2
                    })
                })
            })
            layer.close(index)
        }
    })
}

function sitemapGeneration() {
    if (parseInt($("#maxNumber").val()) > 8) {
        layer.msg("为减少服务器压力，不允许创建操作8层的sitemap生成任务！", {
            icon: 2
        })
        return false
    }
    if ($("#sitemapURL").val() == "" || $("#maxNumber").val() == "") {
        layer.msg("为减少服务器压力，不允许创建操作8层的sitemap生成任务！", {
            icon: 2
        })
        return false
    }
    $("#sitemapGenerationBTN").attr("disabled", true)
    $("#downloadSitemapBTN").hide(200)
    requestPlugin("sitemapGeneration", {
        url: $("#sitemapURL").val(),
        maxNumber: $("#maxNumber").val()
    }, function (rdata) {
        task_stat()
        layer.msg(rdata.msg, {
            icon: rdata.status ? 1 : 2
        })
        if (rdata.status) {
            sitemapGenerationIntervalID = setInterval(function () {
                getSitemapGenerationResult()
            }, 3000)
            document.cookie = "sitemapGenerationIntervalID=" + sitemapGenerationIntervalID
        } else {
            $("#sitemapGenerationBTN").attr("disabled", false)
        }

    })
}

function getSitemapGenerationResult() {
    requestPlugin("getSitemapGenerationStatus", "", function (rdata) {
        if (rdata.status) {
            $("#sitemapGenerationBTN").attr("disabled", false)
            clearInterval(parseInt(getCookie('sitemapGenerationIntervalID')))
            delCookie('sitemapGenerationIntervalID')
            $("#sitemapGenerationResult").val(rdata.data)
            $("#downloadSitemapBTN").show(200)
        } else {
            var index = layer.msg('正在处理中，请耐心等待！', {
                icon: 16,
                time: 0
            });
        }
    })
}

function downloadSitemap() {
    window.open("/my_toolbox/static/sitemap.xml?kagamine=" + randomNumBoth(100000000000, 999999999999), "_blank");
}

function startScan() {
    if ($("#serverIp").val() == "" || $("#portStart").val() == "" || $("#portEnd").val() == "") {
        layer.msg("抱歉，输入的值存在错误", {
            icon: 2
        })
        return false
    }
    $("#startScanBTN").attr("disabled", true)
    requestPlugin("startScanPort", {
        serverIp: $("#serverIp").val(),
        portStart: $("#portStart").val(),
        portEnd: $("#portEnd").val()
    }, function (rdata) {
        task_stat()
        layer.msg(rdata.msg, {
            icon: rdata.status ? 1 : 2
        })
        if (rdata.status) {
            scanIntervalID = setInterval(function () {
                getScanResult()
            }, 3000)
            document.cookie = "scanIntervalID=" + scanIntervalID
        } else {
            $("#startScanBTN").attr("disabled", false)
        }
    })
}

function backToScan() {
    $("#portFormBody").empty()
    $("#portScanResultTable").hide(200, function () {
        $("#scanPortForm").show(200)
    })
}

function switchToHostsFileEdit() {
    getHostsFile()
    $("#hostsList").hide(200, function () {
        $("#hostsEditor").show(200)
    })
}

function backToHostsList() {
    getHostsList()
    $("#hostsEditor").hide(200, function () {
        $("#hostsList").show(200)
    })
}

function backToPreviousPage(type) {
    $("#executionResult").val("")
    switch ($("#commandExecutionResult").attr("from")) {
        case "commandExecution":
            $("#commandExecutionResult").hide(200, function () {
                $("#commandExecution").show(200)
            })
            break;
        case "websiteStressTest":
            $("#commandExecutionResult").hide(200, function () {
                $("#websiteStressTest").show(200)
            })
            break
        case "diskTools":
            $("#commandExecutionResult").hide(200, function () {
                $("#diskTools").show(200)
            })
            break
        default:
            break;
    }
}

function getScanResult() {
    requestPlugin("getScanResult", "", function (rdata) {
        if (rdata.status) {
            $("#startScanBTN").attr("disabled", false)
            clearInterval(parseInt(getCookie('scanIntervalID')))
            delCookie('scanIntervalID')
            $("#portFormBody").empty()
            if (rdata.data.length > 0) {
                for (var i = 0, l = rdata.data.length; i < l; i++) {
                    var $trTemp = $("<tr></tr>")
                    $trTemp.append("<td>" + rdata.data[i].port + "</td>")
                    $trTemp.append("<td>" + rdata.data[i].status + "</td>")
                    $trTemp.append("<td>" + rdata.data[i].type + "</td>")
                    $("#portFormBody").append($trTemp);
                }
                $("#scanPortForm").hide(200, function () {
                    $("#portScanResultTable").show(200)
                })
            } else {
                layer.msg("没有任何开放端口", {
                    icon: 2
                })
            }
        } else {
            var index = layer.msg('正在扫描中，请耐心等待！', {
                icon: 16,
                time: 0
            });
        }
    })
}

function randomNumBoth(Min, Max) {
    var Range = Max - Min;
    var Rand = Math.random();
    var num = Min + Math.round(Rand * Range);
    return num;
}

function setCookie(cname, cvalue, exdays) {
    var d = new Date();
    d.setTime(d.getTime() + (exdays * 24 * 60 * 60 * 1000));
    var expires = "expires=" + d.toGMTString();
    document.cookie = cname + "=" + cvalue + "; " + expires;
}

function getCookie(name) {
    var arr, reg = new RegExp("(^| )" + name + "=([^;]*)(;|$)");
    if (arr = document.cookie.match(reg))
        return unescape(arr[2]);
    else
        return null;
}

function delCookie(name) {
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval = getCookie(name);
    if (cval != null)
        document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
}

function getHostsList() {
    requestPlugin("getHostsList", "", function (rdata) {
        if (rdata.status) {
            $("#hostsFormBody").empty()
            if (rdata.data.length > 0) {
                for (var i = 0, l = rdata.data.length; i < l; i++) {
                    var $trTemp = $("<tr></tr>")
                    $trTemp.append("<td>" + rdata.data[i].ip + "</td>")
                    $trTemp.append("<td>" + rdata.data[i].domain + "</td>")
                    $trTemp.append("<td><button class='btn btn-success btn-sm' onclick='editHosts(\"" + rdata.data[i].ip + "\",\"" + rdata.data[i].domain + "\",\"" + rdata.data[i].original + "\")'>修改</button> <button class='btn btn-danger btn-sm' onclick='deleteHosts(\"" + rdata.data[i].original + "\")'>删除</button></td>")
                    $("#hostsFormBody").append($trTemp);
                }
            }
        } else {
            layer.msg(rdata.msg, {
                icon: rdata.status ? 1 : 2
            })
            switchToHostsFileEdit()
        }
    })
}

function getDiskInfo() {
    requestPlugin("getDiskInfo", "", function (rdata) {
        if (rdata.status) {
            $("#disksFormBody").empty()
            systemPath = ['/etc', '/', '/root', '/var', '/boot', '/home', '/bin', '/dev', '/srv', '/usr', '/lib', '/lib64', '/sys', '/proc', '/sbin']
            for (var i = 0; i < rdata.data.length; i++) {
                if (rdata.data[i].partition.length == 0) {
                    diskInfo = rdata.data[i]
                    var $trTemp = $("<tr></tr>")
                    $trTemp.append("<td class='line-limit-length' title='" + rdata.data[i].device + "' style='max-width:120px'>" + rdata.data[i].device + "</td>")
                    $trTemp.append("<td class='line-limit-length' title='硬盘' style='max-width:120px'>硬盘</td>")
                    $trTemp.append("<td class='line-limit-length' style='max-width:40px'>-</td>")
                    $trTemp.append("<td class='line-limit-length'>" + rdata.data[i].size_gb + "GB</td>")
                    $trTemp.append("<td>-</td>")
                    $trTemp.append("<td><button class='btn btn-success btn-sm' onclick='mountNewDisk(\"" + rdata.data[i].device + "\")'>一键挂载</button>")
                    $("#disksFormBody").append($trTemp);
                } else {
                    for (var j = 0; j < rdata.data[i].partition.length; j++) {
                        partitionInfo = rdata.data[i].partition[j]
                        mountpoint = partitionInfo['mountpoint'] == "" ? "-" : partitionInfo['mountpoint']
                        fstype = partitionInfo['fstype'] == "" ? "-" : partitionInfo['fstype']
                        var $trTemp = $("<tr></tr>")
                        $trTemp.append("<td class='line-limit-length' title='" + partitionInfo['device'] + "' style='max-width:120px'>" + partitionInfo['device'] + "</td>")
                        $trTemp.append("<td class='line-limit-length' title='分区' style='max-width:120px'>分区</td>")
                        $trTemp.append("<td class='line-limit-length' title='" + mountpoint + "' style='max-width:40px'>" + mountpoint + "</td>")
                        $trTemp.append("<td class='line-limit-length'>" + rdata.data[i].partition_1[j].size + "</td>")
                        $trTemp.append("<td>" + fstype + "</td>")
                        availableActions = ""
                        if (systemPath.indexOf(mountpoint) > -1) {
                            availableActions = "不允许操作系统目录"
                        } else if (partitionInfo['fstype'].toLowerCase().indexOf("lvm") != -1) {
                            availableActions = "暂不支持LVM"
                        } else if (mountpoint == "/www") {
                            availableActions = "暂不支持迁移宝塔"
                        } else {
                            availableActions += " <button class='btn btn-danger btn-sm' onclick='formatPartition(\"/dev/" + partitionInfo['device'] + "\",\"" + partitionInfo['mountpoint'] + "\")'>格式化分区</button> "
                            if (partitionInfo['fstype'] != "") {
                                if (partitionInfo['mountpoint'] == "") {
                                    availableActions += " <button class='btn btn-success btn-sm' onclick='mountPartition(\"/dev/" + partitionInfo['device'] + "\",\"" + partitionInfo['fstype'] + "\")'>挂载分区</button> "
                                } else {
                                    availableActions += " <button class='btn btn-danger btn-sm' onclick='umountPartition(\"/dev/" + partitionInfo['device'] + "\")'>卸载分区</button> "
                                }
                            }

                        }
                        $trTemp.append("<td>" + availableActions + "</td>")
                        $("#disksFormBody").append($trTemp);
                    }
                }
            }
        } else {
            layer.msg(rdata.msg, {
                icon: rdata.status ? 1 : 2
            })
        }
    })
}

function editHosts(ip, domain, original) {
    layer.open({
        id: 1,
        type: 1,
        title: 'Hosts编辑',
        skin: 'layui-layer-rim',
        area: ['450px', 'auto'],
        content: $("#hostsTemplate").html().replaceAll("hosts", "temp"),
        btn: ['保存', '取消'],
        btn1: function (index, layero) {
            if (original != undefined) {
                requestPlugin("delHosts", {
                    original: original
                }, function (rdata) {
                    getHostsList()
                    layer.msg(rdata.msg, {
                        icon: rdata.status ? 1 : 2
                    })
                })
            }
            requestPlugin("addHosts", {
                ip: $("#tempIP").val(),
                domain: $("#tempDomain").val()
            }, function (rdata) {
                getHostsList()
                layer.msg(rdata.msg, {
                    icon: rdata.status ? 1 : 2
                })
            })
            layer.close(index);
        },
        btn2: function (index, layero) {
            layer.close(index);
        }
    });
    $("#tempIP").val(ip)
    $("#tempDomain").val(domain)
}

function deleteHosts(original) {
    requestPlugin("delHosts", {
        original: original
    }, function (rdata) {
        getHostsList()
        layer.msg(rdata.msg, {
            icon: rdata.status ? 1 : 2
        })
    })
}

function logWrite() {
    requestPlugin("logWrite", {
        logType: $("#logType").val(),
        logDetail: $("#logDetail").val()
    }, function (rdata) {
        getHostsList()
        layer.msg(rdata.msg, {
            icon: rdata.status ? 1 : 2
        })
    })
}

function editHostsFile() {
    $("#portFormBody").empty()
    $("#portScanResultTable").hide(200, function () {
        $("#scanPortForm").show(200)
    })
}

function getHostsFile() {
    requestPlugin("getHostsFile", "", function (rdata) {
        $("#hostEditTextbox").val(rdata.data)
    })
    $("#bashCommand").val()
}

function saveHostsFile() {
    requestPlugin("saveHostsFile", { data: $("#hostEditTextbox").val() }, function (rdata) {
        getHostsFile()
        getHostsList()
        layer.msg(rdata.msg, {
            icon: rdata.status ? 1 : 2
        })
    })
}

function executeCommand(type) {
    if ($("#bashCommand").val() == "") {
        $("#bashCommand").val("echo Vocaloid is ALIVE")
    }
    $("#executeCommandBTN").attr("disabled", true)
    $("#startWebsiteStressTestBTN").attr("disabled", true)
    requestPlugin("executeCommand", {
        bashCommand: $("#bashCommand").val()
    }, function (rdata) {
        task_stat()
        layer.msg(rdata.msg, {
            icon: rdata.status ? 1 : 2
        })
        if (rdata.status) {
            executeCommandIntervalID = setInterval(function () {
                getExecuteResult(type, rdata.logFileName)
            }, 3000)
            document.cookie = "executeCommandIntervalID=" + executeCommandIntervalID
        } else {
            $("#executeCommandBTN").attr("disabled", false)
            $("#startWebsiteStressTestBTN").attr("disabled", false)
        }
    })
    $("#bashCommand").val("")
}

function getExecuteResult(type, logFileName) {
    requestPlugin("getExecuteResult", { logFileName: logFileName }, function (rdata) {
        if (rdata.status) {
            if (rdata.status == 1) {
                $("#executeCommandBTN").attr("disabled", false)
                $("#startWebsiteStressTestBTN").attr("disabled", false)
                $("#commandExecutionResult").attr("from", type);
                $("#executionResult").val(rdata.result)
                switch (type) {
                    case "commandExecution":
                        $("#commandExecution").hide(200, function () {
                            $("#commandExecutionResult").show(200)
                        })
                        break;
                    case "websiteStressTest":
                        $("#websiteStressTest").hide(200, function () {
                            $("#commandExecutionResult").show(200)
                        })
                        break
                    case "diskTools":
                        $("#diskTools").hide(200, function () {
                            $("#commandExecutionResult").show(200)
                        })
                        break
                    default:
                        break;
                }
            } else if (rdata.status == 2) {
                $("#executeCommandBTN").attr("disabled", false)
                $("#startWebsiteStressTestBTN").attr("disabled", false)
            }
            layer.msg(rdata.msg, {
                icon: rdata.status ? 1 : 2
            })
            clearInterval(parseInt(getCookie('executeCommandIntervalID')))
            delCookie('executeCommandIntervalID')
        } else {
            var index = layer.msg('正在执行命令中，请耐心等待！', {
                icon: 16,
                time: 0
            });
        }
    })
}

function cleanCommandBox() {
    $("#bashCommand").val("")
}

function requestPage() {
    if ($("#requestPageUrl").val() == "") {
        layer.msg("请输入你要请求的网页地址~", {
            icon: 3
        })
        return false
    }
    $("#requestPageBTN").attr("disabled", true)
    requestPlugin("requestPage", {
        url: $("#requestPageUrl").val()
    }, function (rdata) {
        $("#requestPageBTN").attr("disabled", false)
        if (rdata.status) {
            $("#requestPageResult").val(rdata.data)
        } else {
            layer.msg(rdata.msg, {
                icon: rdata.status ? 1 : 2
            })
        }
    })
}

function systemDetection(system,callback){
    requestPlugin("systemDetection", {
        system: system
    }, function (rdata) {
        callback(rdata.status)
    })
}

function cleanRequestPageResult() {
    $("#requestPageResult").val("")
    $("#requestPageUrl").val("")
}

function aboutPlugin() {
    if (getCookie("myToolboxFiveStar") == "kagamine") {
        pluginEgg()
    } else {
        layer.open({
            id: 1,
            title: '给个五星呗~~~',
            content: '<center><img style="border-radius:16%; overflow:hidden;" src="/my_toolbox/static/rin.gif"><br><br><p style="color:Grey;font-size:15px;">23333，给个五星呗！</p></center>',
            btn: ['OK！'],
            btn1: function (index, layero) {
                pluginEgg()
                setCookie("myToolboxFiveStar", "kagamine", 7)
                layer.close(index)
            }
        })
    }
}

function pluginEgg() {
    var img = new Image()
    img.src = '/my_toolbox/static/78530939_p1.png'
    img.onerror = function () {
        console.log('Image loading failed')
        return false
    }
    img.onload = function () {
        setTimeout(function () {
            $("#aboutImg").attr('src', '/my_toolbox/static/78530939_p1.png')
        }, 1500);
        setTimeout(function () {
            $("#aboutImg").attr('src', '/my_toolbox/static/about.png')
        }, 1600);
        setTimeout(function () {
            $("#aboutImg").attr('src', '/my_toolbox/static/78530939_p1.png')
        }, 1670);
        setTimeout(function () {
            layer.msg('Kagamine Yes！', {
                icon: 1
            })
        }, 1670);
    }
}

function donate() {
    layer.open({
        type: 1,
        title: "支持作者",
        area: '800px;',
        content: '<center><img src="https://static.llilii.cn/images/donate.png"/></center>',
        yes: function (index) {
            callback()
            layer.close(index)
        }
    })
}

function loadImage(url) {
    var img = new Image()
    img.src = url
    img.onerror = function () {
        console.log('Image loading failed')
        return false
    }
}

function requestPlugin(functionName, args, callback, timeout) {
    var index = layer.msg('正在处理,请稍后...', {
        icon: 16,
        time: 0
    })
    pluginName = 'my_toolbox'
    if (!timeout) timeout = 36000;
    $.ajax({
        type: 'POST',
        url: '/plugin?action=a&s=' + functionName + '&name=' + pluginName,
        data: args,
        timeout: timeout,
        async: true,
        success: function (rdata) {
            layer.close(index)
            if (rdata.status) {
                if (rdata.status == -1) {
                    rdata.status = 0
                }
                if (callback) {
                    return callback(rdata)
                } else {
                    setTimeout(function () {
                        layer.msg(rdata.msg, {
                            icon: rdata.status ? 1 : 2
                        })
                    }, 10)
                    return true
                }
            } else {
                /*
                $("#pluginMain").hide(200)
                $("#fatalError").show(100)
                $('.layui-layer-page').css({
                    'width': '300px'
                });
                layer.msg(rdata.msg, {
                    icon: 2
                })
                */
            }
        },
        error: function (ex) {
            layer.close(index)
            if (!callback) {
                layer.msg('请求过程发现错误!', {
                    icon: 2
                });
                return;
            }
            return callback(ex);
        }
    });
}