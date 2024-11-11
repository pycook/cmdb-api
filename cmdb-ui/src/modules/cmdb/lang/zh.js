const cmdb_zh = {
    relation: '关系',
    attribute: '属性',
    configTable: '配置表格',
    enterpriseVersionFlag: '企',
    enterpriseVersionTip: '仅限企业版',
    menu: {
        views: '视图',
        topologyView: '拓扑视图',
        resources: '资源',
        config: '配置',
        backend: '管理',
        ciTable: '资源数据',
        ciTree: '资源层级',
        ciSearch: '资源搜索',
        adCIs: '自动发现池',
        preference: '我的订阅',
        batchUpload: '批量导入',
        citypeManage: '模型配置',
        backendManage: '后台管理',
        customDashboard: '定制仪表盘',
        serviceTreeDefine: '服务树定义',
        citypeRelation: '模型关系',
        operationHistory: '操作审计',
        relationType: '关系类型',
        ad: '自动发现',
        cidetail: 'CI 详情',
        scene: '场景'
    },
    ciType: {
        ciType: '模型',
        attributes: '模型属性',
        relation: '模型关联',
        trigger: '触发器',
        autoDiscoveryTab: '自动发现',
        attributeAD: '属性自动发现',
        relationAD: '关系自动发现',
        grant: '权限配置',
        addGroup: '新增分组',
        editGroup: '修改分组',
        group: '分组',
        attributeLibray: '属性库',
        viewAttributeLibray: '查看属性库',
        addGroup2: '添加分组',
        modelExport: '模型导出',
        filename: '文件名',
        filenameInputTips: '请输入文件名',
        selectModel: '请选择模型',
        unselectModel: '未选',
        selectedModel: '已选',
        addCITypeInGroup: '在该组中新增CI模型',
        addCIType: '新增CI模型',
        editGroupName: '重命名分组',
        deleteGroup: '删除该组',
        CITypeName: '模型名(英文)',
        English: '英文',
        inputAttributeName: '请输入属性名',
        attributeNameTips: '不能以数字开头，可以是英文 数字以及下划线 (_)',
        editCIType: '编辑模型',
        defaultSort: '默认排序',
        selectDefaultOrderAttr: '选择默认排序属性',
        asec: '正序',
        desc: '倒序',
        uniqueKey: '唯一标识',
        uniqueKeySelect: '请选择唯一标识',
        uniqueKeyTips: 'json、密码、计算属性、下拉列表属性不能作为唯一标识',
        notfound: '找不到想要的?',
        cannotDeleteGroupTips: '该分组下有数据, 不能删除!',
        confirmDeleteGroup: '确定要删除分组 【{groupName}】 吗？',
        confirmDeleteCIType: '确定要删除模型 【{typeName}】 吗？',
        uploading: '正在导入中',
        uploadFailed: '导入失败，请稍后重试',
        addPlugin: '新建plugin',
        deletePlugin: '删除plugin',
        confirmDeleteADT: '确认删除 【{pluginName}】',
        attributeMap: '字段映射',
        nodeConfig: '节点配置',
        autoDiscovery: '自动发现属性',
        node: '节点',
        adExecConfig: '执行配置',
        adExecTarget: '执行机器',
        oneagentIdTips: '请输入以0x开头的16进制OneAgent ID',
        selectFromCMDBTips: '从CMDB中选择 ',
        adAutoInLib: '自动入库',
        adAutoInLibTip: '发现的实例直接入库成CI',
        adInterval: '采集频率',
        byInterval: '按间隔',
        allNodes: '所有机器',
        specifyNodes: '指定机器',
        masterNode: 'Master机器',
        masterNodeTip: '安装OneMaster的所在机器',
        specifyNodesTips: '请填写指定机器！',
        username: '用户名',
        password: '密码',
        link: '链接',
        list: '多值',
        listTips: '属性的值是1个或者多个，接口返回的值的类型是list',
        computeForAllCITips: '所有CI触发计算',
        confirmcomputeForAllCITips: '确认触发所有CI的计算？',
        isUnique: '是否唯一',
        unique: '唯一',
        isChoice: '是否选择',
        defaultShow: '默认显示',
        defaultShowTips: 'CI实例表格默认展示该字段',
        isSortable: '可排序',
        isIndex: '是否索引',
        index: '索引',
        indexTips: '属性可被用于全文检索，加速查询',
        confirmDelete: '确认删除【{name}】?',
        confirmDelete2: '确认删除?',
        computeSuccess: '触发成功！',
        basicConfig: '基础设置',
        AttributeName: '属性名(英文)',
        DataType: '数据类型',
        defaultValue: '默认值',
        autoIncID: '自增ID',
        customTime: '自定义时间',
        advancedSettings: '高级设置',
        font: '字体',
        color: '颜色',
        choiceValue: '下拉列表',
        computedAttribute: '计算属性',
        computedAttributeTips: '该属性的值是通过模型的其它属性构建的表达式或者执行一段代码的方式计算而来，属性的引用方法为: {{ 属性名 }}',
        addAttribute: '新增属性',
        existedAttributes: '已有属性',
        editAttribute: '编辑属性',
        addAttributeTips1: '选中排序，则必须也要选中！',
        uniqueConstraint: '唯一校验',
        up: '上移',
        down: '下移',
        selectAttribute: '添加属性',
        groupExisted: '分组名称已存在',
        attributeSortedTips: '其他分组中的属性不能进行排序，如需排序请先拖至自定义的分组！',
        attributeSortedTips2: '非继承属性不能插入到继承属性前！',
        buildinAttribute: '内置字段',
        expr: '表达式',
        code: '代码',
        apply: '应用',
        continueAdd: '继续添加',
        filter: '过滤',
        choiceOther: '其他模型属性',
        choiceWebhookTips: '返回的结果按字段来过滤，层级嵌套用##分隔，比如k1##k2，web请求返回{k1: [{k2: 1}, {k2: 2}]}, 解析结果为[1, 2]',
        selectCIType: '请选择CMDB模型',
        selectCITypeAttributes: '请选择模型属性',
        selectAttributes: '请选择属性',
        choiceScriptDemo: 'class ChoiceValue(object):\n    @staticmethod\n    def values():\n        """\n        执行入口, 返回下拉列表\n        :return: 返回一个列表, 值的类型同属性的类型\n        例如:\n        return ["在线", "下线"]\n        """\n        return []',
        valueExisted: '当前值已存在！',
        addRelation: '新增关系',
        sourceCIType: '源模型',
        sourceCITypeTips: '请选择源模型',
        dstCIType: '目标模型',
        dstCITypeTips: '请选择目标模型',
        relationType: '关联类型',
        relationTypeTips: '请选择关联类型',
        isParent: '被',
        relationConstraint: '关系约束',
        relationConstraintTips: '请选择关系约束',
        one2Many: '一对多',
        one2One: '一对一',
        many2Many: '多对多',
        basicInfo: '基本信息',
        nameInputTips: '请输入名称',
        triggerDataChange: '数据变更',
        triggerDate: '日期属性',
        triggerEnable: '开启',
        descInput: '请输入描述',
        triggerCondition: '触发条件',
        addInstance: '新增实例',
        deleteInstance: '删除实例',
        changeInstance: '实例变更',
        selectMutipleAttributes: '请选择属性（多选）',
        selectSingleAttribute: '请选择属性（单选）',
        beforeDays: '提前',
        days: '天',
        notifyAt: '发送时间',
        notify: '通知',
        triggerAction: '触发动作',
        receivers: '收件人',
        emailTips: '请输入邮箱，多个邮箱用;分隔',
        customEmail: '自定义收件人',
        notifySubject: '通知标题',
        notifySubjectTips: '请输入通知标题',
        notifyContent: '内容',
        notifyMethod: '通知方式',
        botSelect: '请选择机器人',
        refAttributeTips: '标题、内容可以引用该模型的属性值，引用方法为: {{ attr_name }}',
        webhookRefAttributeTips: '请求参数可以引用该模型的属性值，引用方法为: {{ attr_name }}',
        newTrigger: '新增触发器',
        editTriggerTitle: '编辑触发器 {name}',
        newTriggerTitle: '新增触发器 {name}',
        confirmDeleteTrigger: '确认删除该触发器吗?',
        int: '整数',
        float: '浮点数',
        longText: '长文本',
        shortText: '短文本',
        shortTextTip: '文本长度 <= 128',
        referenceModel: '引用模型',
        referenceModelTip: '请选择引用模型',
        referenceModelTip1: '用于快捷查看引用模型实例',
        bool: '布尔',
        reference: '引用',
        text: '文本',
        datetime: '日期时间',
        date: '日期',
        time: '时间',
        json: 'JSON',
        event: '事件',
        reg: '正则校验',
        isInherit: '是否继承',
        inheritType: '继承模型',
        inheritTypePlaceholder: '请选择继承模型（多选）',
        inheritFrom: '属性继承自{name}',
        groupInheritFrom: '请至{name}进行修改',
        downloadType: '下载模型',
        deleteCIType: '删除模型',
        otherGroupTips: '其他分组属性不可排序',
        filterTips: '点击可仅查看{name}属性',
        attributeAssociation: '属性关联',
        attributeAssociationTip1: '通过2个模型的属性值(除密码、json、多值、长文本、布尔、引用)来自动建立关系',
        attributeAssociationTip2: '双击可编辑',
        attributeAssociationTip3: '属性关联必须选择两个属性',
        attributeAssociationTip4: '请选择原模型属性',
        attributeAssociationTip5: '请选择目标模型属性',
        attributeAssociationTip6: '不可再删除',
        show: '展示属性',
        setAsShow: '设置为展示属性',
        cancelSetAsShow: '取消设置为展示属性',
        showTips: '服务树和拓扑视图里节点的名称',
        isDynamic: '动态属性',
        dynamicTips: '譬如监控类的数据, 频繁更新的数据, 建议设置为动态属性, 则不会记录该属性的变更历史',
        cloudAccessKey: '公有云AccessKey',
        cloudAccessKeyTip: '用于系统在不安装Agent的情况下同步公有云信息',
        configCheckTitle: '健康检查',
        checkTestTip: '检查前请先保存配置',
        checkTestBtn: '执行机器同步规则检查',
        checkTestTip2: '点击查看发现规则在执行机器上的同步状态，系统每5分钟同步一次，若状态为异常，可查看可能的问题',
        checkTestBtn1: '自动发现测试',
        checkTestTip3: '点击按钮，系统将在一台机器上执行自动发现规则',
        checkModalTitle: '执行机器同步规则检查',
        checkModalTip: '若状态为下线，请按以下操作检查Agent',
        checkModalTip1: '1. 检查OneAgent进程是否存活',
        checkModalTip2: '2. 查看OneAgent的日志，每5分钟有自动发现规则同步的日志',
        checkModalColumn1: '执行机器',
        checkModalColumn2: 'AgentID',
        checkModalColumn3: '状态',
        checkModalColumnStatus1: '在线',
        checkModalColumnStatus2: '下线',
        checkModalColumn4: '最近检查时间',
        testModalTitle: '自动发现测试',
        attrMapTableAttrPlaceholder: '请编辑名称',
        nodeSettingIp: '网络设备IP地址',
        nodeSettingIpTip: '请输入 ip 地址',
        nodeSettingIpTip1: 'ip地址格式错误',
        nodeSettingCommunity: 'Community',
        nodeSettingCommunityTip: '请输入 community',
        nodeSettingVersion: '版本',
        nodeSettingVersionTip: '请选择版本',
        cronRequiredTip: '采集频率不能为空',
        relationADTip: '关系自动发现的前提是配置有属性自动发现',
        relationADHeader1: '自动发现属性',
        relationADHeader2: '关联模型属性',
        relationADSelectAttr: '请选择自动发现的属性',
        relationADSelectCIType: '请选择与本模型关联的模型',
        relationADSelectModelAttr: '请选择关联模型属性',
        relationADTip2: '当自动发现属性与关联模型属性一致时，两实例模型则自动关联',
        relationADTip3: '如果自动发现的属性值是列表，则会和关联模型建立多个关系',
        deleteRelationAdTip: '不可再删除',
        cronTips: '格式同crontab, 例如：0 15 * * 1-5',
        privateCloud: 'vSphere API配置',
        host: '地址',
        account: '账号',
        insecure: '是否证书验证',
        vcenterName: '虚拟平台名',
        resourceSearchTip1: '请使用条件过滤进行CI筛选，并将过滤表达式复制粘贴到上一步填写框中。',
        resourceSearchTip2: '注1：请使用表达式右侧的绿色按钮进行复制',
        resourceSearchTip3: '注2：如不需要筛选，请直接点击灰色按钮进行复制粘贴，即可配置为所有节点',
        enable: '开启',
        enableTip: '确定切换开启状态吗',
        portScanConfig: '端口扫描配置',
        portScanLabel1: 'CIDR',
        portScanLabel2: '端口范围',
        portScanLabel3: 'AgentID',
        viewAllAttr: '查看所有属性',
        attrGroup: '属性分组',
        attrName: '属性名称',
        attrAlias: '属性别名',
        attrCode: '属性代码',
        computedAttrTip1: '引用属性遵循jinja2语法',
        computedAttrTip2: `多值属性(列表)默认呈现包括[ ], 如果要去掉, 引用方法为: """{{ attr_name | join(',') }}"""  其中逗号为分隔符`,
        computedAttrTip3: `不能引用其他计算属性`,
        example: '例如',
        attrFilterTip: '第三列值可选择本模型的属性，来实现级联属性的功能',
        rule: '规则',
        cascadeAttr: '级联',
        cascadeAttrTip: '级联属性注意顺序',
        enumValue: '枚举值',
        label: '标签',
        valueInputTip: '请输入枚举值',
        enumValueTip2: '枚举值不能重复',
        builtin: '内置',
        department: '部门',
        user: '用户',
        userGroup: '用户组',
        departmentTip: '下拉选择为通用设置公司架构里的所有部门',
        userGroupSelectTip: '请选择用户组',
        displayValue: '展示值',
        displayValueSelectTip: '请选择展示值',
        departmentCascadeDisplay: '部门级联显示',
        filterUsers: '筛选用户',
        enum: '枚举',
        ciGrantTip: `筛选条件可使用{{}}引用变量实现动态变化，目前支持用户变量，如{{user.uid}},{{user.username}},{{user.email}},{{user.nickname}}`,
        searchInputTip: '请搜索资源关键字',
        resourceSearch: '资源搜索',
        recentSearch: '最近搜索',
        myCollection: '我的收藏',
        keyword: '关键字',
        CIType: '模型',
        filterPopoverLabel: '条件过滤',
        conditionFilter: '条件过滤',
        advancedFilter: '高级筛选',
        saveCondition: '保存条件',
        confirmClear: '确认清空?',
        currentPage: '当前页'
    },
    components: {
        unselectAttributes: '未选属性',
        selectAttributes: '已选属性',
        downloadCI: '导出数据',
        filename: '文件名',
        filenameInputTips: '请输入文件名',
        saveType: '保存类型',
        saveTypeTips: '请选择保存类型',
        xlsx: 'Excel工作簿(*.xlsx)',
        csv: 'CSV(逗号分隔)(*.csv)',
        html: '网页(*.html)',
        xml: 'XML数据(*.xml)',
        txt: '文本文件(制表符分隔)(*.txt)',
        grantUser: '授权用户/部门',
        grantRole: '授权角色',
        confirmRevoke: '确认删除 【{name}】 的 【授权】 权限？',
        readAttribute: '查看字段',
        readCI: '查看实例',
        config: '配置',
        ciTypeGrant: '模型权限',
        ciGrant: '实例权限',
        attributeGrant: '字段权限',
        relationGrant: '关系权限',
        perm: '权限',
        all: '全部',
        customize: '自定义',
        none: '无',
        customizeFilterName: '请输入自定义筛选条件名',
        colorPickerError: '初始化颜色格式错误，使用#fff或rgb格式',
        example: '示例值',
        aliyun: '阿里云',
        tencentcloud: '腾讯云',
        huaweicloud: '华为云',
        beforeChange: '变更前',
        afterChange: '变更后',
        noticeContentTips: '请输入通知内容',
        saveQuery: '保存条件',
        pleaseSearch: '请查找',
        conditionFilter: '条件过滤',
        attributeDesc: '属性说明',
        ciSearchTips: '1. json、密码、链接、长文本、引用属性不能搜索\n2. 搜索内容包括逗号, 则需转义\n3. 只搜索索引属性, 非索引属性使用条件过滤',
        ciSearchTips2: '例: q=hostname:*0.0.0.0*',
        subCIType: '订阅模型',
        already: '已',
        not: '未',
        sub: '订阅',
        selectBelow: '请在下方进行选择',
        subSuccess: '订阅成功',
        subFailed: '订阅失败，请稍后再试',
        selectMethods: '请选择方式',
        noAuthRequest: '暂无请求认证',
        noParamRequest: '暂无参数认证',
        requestParam: '请求参数',
        param: '参数{param}',
        value: '值{value}',
        clear: '清空',
        updater: '更新人',
        updateTime: '更新时间',
        default: '默认'
    },
    batch: {
        downloadFailed: '失败下载',
        unselectCIType: '尚未选择模板类型',
        pleaseUploadFile: '请上传文件',
        batchUploadCanceled: '批量上传已取消',
        selectCIType: '选择模型',
        selectCITypeTips: '请选择模型后下载模板',
        downloadTemplate: '下载模板',
        clickDownload: '点击下载',
        supportFileTypes: '支持文件类型：xls，xlsx',
        uploadResult: '上传结果',
        total: '共',
        successItems: '条，已成功',
        failedItems: '条，失败',
        items: '条',
        errorTips: '错误信息',
        requestFailedTips: '请求出现错误，请稍后再试',
        requestSuccessTips: '批量上传已完成',
        uploadFile: '文件上传',
        drawTips1: '请先<span class="cmdb-batch-upload-tips">选择模型</span>，<span class="cmdb-batch-upload-tips">下载模板</span>后',
        drawTips2: '<span class="cmdb-batch-upload-tips">点击或拖拽文件</span>至此上传',
        dataPreview: '数据预览并导入',
        tips1: '温馨提示：',
        tips2: '1. 点击下载模板，用户可以自定义模板文件的表头，包括模型属性、模型关联',
        // eslint-disable-next-line no-template-curly-in-string
        tips3: '2. 模板文件中红色为模型关系，如$产品.产品名(${模型名}.{属性名})这一列就可建立和产品之间的关系',
        tips4: '3. 下载模板excel文件中会将属性的下拉列表枚举配置置为下拉选项，请注意，受excel本身的限制，单个下拉框限制了最多255个字符，如果超过255个字符，我们不会设置该属性的下拉选项',
        tips5: '4. 在使用excel模板时，请确保单个文件不超过5000行',
    },
    preference: {
        mySub: '我的订阅',
        sub: '订阅',
        cancelSub: '取消订阅',
        editSub: '编辑订阅',
        peopleSub: '位同事已订阅',
        noSub: '暂无同事订阅',
        cancelSubSuccess: '取消订阅成功',
        confirmcancelSub: '确认取消订阅',
        confirmcancelSub2: '确认取消订阅 {name} 吗?',
        of: '的',
        hoursAgo: '小时前',
        daysAgo: '天前',
        monthsAgo: '月前',
        yearsAgo: '年前',
        just: '刚刚',
        searchPlaceholder: '请搜索模型',
        subCITable: '数据订阅',
        subCITree: '层级订阅',
    },
    custom_dashboard: {
        charts: '图表',
        newChart: '新增图表',
        editChart: '编辑图表',
        title: '标题',
        titleTips: '请输入图表标题',
        calcIndicators: '计算指标',
        dimensions: '维度',
        selectDimensions: '请选择维度',
        quantity: '数量',
        childCIType: '关系模型',
        level: '层级',
        levelTips: '请输入关系层级',
        preview: '预览',
        showIcon: '是否显示icon',
        chartType: '图表类型',
        dataFilter: '数据筛选',
        format: '格式',
        fontColor: '字体颜色',
        backgroundColor: '背景颜色',
        chartColor: '图表颜色',
        chartLength: '图表长度',
        barType: '柱状图类型',
        stackedBar: '堆积柱状图',
        multipleSeriesBar: '多系列柱状图',
        axis: '轴',
        direction: '方向',
        lowerShadow: '下方阴影',
        count: '指标',
        bar: '柱状图',
        line: '折线图',
        pie: '饼状图',
        table: '表格',
        default: '默认',
        relation: '关系',
        noCustomDashboard: '管理员暂未定制仪表盘',
    },
    preference_relation: {
        newServiceTree: '新增服务树',
        editServiceTree: '编辑服务树',
        serviceTreeName: '服务树名',
        serviceTreeNamePlaceholder: '请输入服务树名',
        public: '公开',
        saveLayout: '保存布局',
        childNodesNotFound: '不存在子节点，不能形成业务关系，请重新选择！',
        tips1: '不能与当前选中节点形成视图，请重新选择！',
        tips2: '请输入新增服务树名！',
        tips3: '请选择至少两个节点！',
        tips4: '树子节点为必选',
        tips5: '选中树目录节点，服务树子节点展示成Table',
        showLeafNode: '树的子节点展示成Table',
        showTreeNode: '展示树节点信息',
        sort: '顺序',
        sort1: '树子节点信息在前',
        sort2: '树节点信息在前'

    },
    history: {
        ciChange: 'CI变更',
        relationChange: '关系变更',
        ciTypeChange: '模型变更',
        triggerHistory: '触发历史',
        opreateTime: '操作时间',
        user: '用户',
        userTips: '输入筛选用户名',
        filter: '筛选',
        filterOperate: '筛选操作',
        attribute: '属性',
        old: '旧',
        new: '新',
        noUpdate: '没有修改',
        itemsPerPage: '/页',
        triggerName: '触发器名称',
        event: '事件',
        action: '动作',
        status: '状态',
        done: '已完成',
        undone: '未完成',
        triggerTime: '触发时间',
        totalItems: '共 {total} 条记录',
        pleaseSelect: '请选择',
        startTime: '开始时间',
        endTime: '结束时间',
        deleteCIType: '删除模型',
        addCIType: '新增模型',
        updateCIType: '修改模型',
        addAttribute: '新增属性',
        updateAttribute: '修改属性',
        deleteAttribute: '删除属性',
        addTrigger: '新增触发器',
        updateTrigger: '修改触发器',
        deleteTrigger: '删除触发器',
        addUniqueConstraint: '新增联合唯一',
        updateUniqueConstraint: '修改联合唯一',
        deleteUniqueConstraint: '删除联合唯一',
        addRelation: '新增关系',
        deleteRelation: '删除关系',
        noModifications: '没有修改',
        attr: '属性名',
        attrId: '属性ID',
        changeDescription: '属性ID：{attr_id}，提前：{before_days}天，主题：{subject}\n内容：{body}\n通知时间：{notify_at}',
        ticketStartTime: '工单发起时间',
        ticketCreator: '发起人',
        ticketTitle: '工单名称',
        ticketFinishTime: '节点完成时间',
        ticketNodeName: '节点名称',
        itsmUninstalled: '请结合维易ITSM使用',
        applyItsm: '免费申请',
        ticketId: '工单ID',
        addReconciliation: '新增合规检查',
        updateReconciliation: '修改合规检查',
        deleteReconciliation: '删除合规检查',
    },
    relation_type: {
        addRelationType: '新增关系类型',
        nameTips: '请输入类型名',
    },
    ad: {
        upload: '规则导入',
        download: '规则导出',
        accept: '入库',
        acceptBy: '入库人',
        acceptTime: '入库时间',
        confirmAccept: '确认入库？',
        acceptSuccess: '入库成功',
        isAccept: '入库',
        deleteADC: '确认删除该条数据？',
        batchDelete: '确认删除这些数据？',
        agent: '服务器',
        snmp: '网络设备',
        http: '公有云',
        component: '数据库 & 中间件',
        privateCloud: '私有云',
        rule: '自动发现规则',
        timeout: '超时错误',
        mode: '模式',
        collectSettings: '采集设置',
        updateFields: '更新字段',
        pluginScript: `# -*- coding:utf-8 -*-

import json
        
        
class AutoDiscovery(object):
        
    @property
    def unique_key(self):
        """
        
        :return: Returns the name of a unique attribute
        """
        return
        
    @staticmethod
    def attributes():
        """
        Define attribute fields
        :return: Returns a list of attribute fields. The list items are (name, type, description). The name must be in English.
        type: String Integer Float Date DateTime Time JSON Bool Reference
        For example:
        return [
            ("ci_type", "String", "CIType name"),
            ("private_ip", "String", "Internal IP, multiple values separated by commas")
        ]
        """
        return []
        
    @staticmethod
    def run():
        """
        Execution entry, returns collected attribute values
        :return: 
        Returns a list, the list item is a dictionary, the dictionary key is the attribute name, and the value is the attribute value
        For example:
        return [dict(ci_type="server", private_ip="192.168.1.1")]
        """
        return []
        
        
if __name__ == "__main__":
    result = AutoDiscovery().run()
    if isinstance(result, list):
        print("AutoDiscovery::Result::{}".format(json.dumps(result)))
    else:
        print("ERROR: The collection return must be a list")
        `,
        server: '物理机',
        vserver: '虚拟机',
        nic: '网卡',
        disk: '硬盘',
        httpSearchPlaceHolder: '请输入关键词',
        corporateTip: '更多类型见企业版，有需要请与我们联系 ',
        ruleCount: '规则数',
        execMachine: '执行机器数',
        resource: '自动发现资源数',
        autoInventory: '入库数',
        newThisWeek: '本周新增',
        newThisMonth: '本月新增',
        log: '日志',
        discoveryCardResoureTip: '自动发现的资源类型数',
        addPlugin: '新增插件',
        pluginSearchTip: '请搜索规则',
        innerFlag: '内置',
        defaultName: '默认名称',
        deleteTip: '不可再删除',
        tabCustom: '自定义',
        tabConfig: '已有配置',
        addConfig: '添加配置',
        configErrTip: '请选择配置'
    },
    ci: {
        attributeDesc: '查看属性配置',
        selectRows: '选取：{rows} 项',
        addRelation: '添加关系',
        viewRelation: '查看关系',
        all: '全部',
        batchUpdate: '批量修改',
        batchUpdateConfirm: '确认要批量修改吗？',
        batchUpdateInProgress: '正在批量修改',
        batchUpdateInProgress2: '正在批量修改，共{total}个，成功{successNum}个，失败{errorNum}个',
        batchDeleting: '正在删除...',
        batchDeleting2: '正在删除，共{total}个，成功{successNum}个，失败{errorNum}个',
        copyFailed: '复制失败！',
        noLevel: '无层级关系！',
        batchAddRelation: '批量添加关系',
        history: '变更记录',
        relITSM: '关联工单',
        topo: '拓扑',
        table: '表格',
        m2mTips: '当前模型关系为多对多，请前往关系视图进行增删操作',
        confirmDeleteRelation: '确认删除关系？',
        tips1: '多个值使用,分割',
        tips2: '可根据需要修改字段，当值为 空 时，则该字段 置空',
        tips3: '请选择需要修改的字段',
        tips4: '必须至少选择一个字段',
        tips5: '搜索 名称 | 别名',
        tips6: '加快检索, 可以全文搜索, 无需使用条件过滤\n\n json、链接、密码目前不支持建索引 \n\n文本字符长度超过190不能建索引',
        tips7: '是否配置下拉列表',
        tips8: '多值, 比如内网IP',
        tips9: '仅针对前端',
        tips10: '模型的其他属性通过表达式的方式计算出来\n\n一个代码片段计算返回的值',
        newUpdateField: '新增修改字段',
        attributeSettings: '字段设置',
        share: '分享',
        noPermission: '暂无权限',
        rollback: '回滚',
        rollbackHeader: '实例回滚',
        rollbackTo: '回滚至: ',
        rollbackToTips: '请选择回滚时间点',
        baselineDiff: '基线对比结果',
        instance: '实例',
        rollbackBefore: '当前值',
        rollbackAfter: '回滚后',
        noDiff: '在【{baseline}】后数据没有发生变化',
        rollbackConfirm: '确认要回滚吗 ？',
        rollbackSuccess: '回滚成功',
        rollbackingTips: '正在批量回滚中',
        batchRollbacking: '正在回滚，共{total}个，成功{successNum}个，失败{errorNum}个',
        baselineTips: '该时间点的变更也会被回滚, 唯一标识、密码属性、动态属性不支持回滚',
        cover: '覆盖',
    },
    serviceTree: {
        remove: '移除',
        deleteNode: '移除 {name}',
        tips1: '例：q=os_version:centos&sort=os_version',
        tips2: '表达式搜索',
        alert1: '管理员 还未配置业务关系, 或者你无权限访问!',
        copyFailed: '复制失败',
        deleteRelationConfirm: '确认将选中的 {name} 从当前关系中删除？',
        batch: '批量操作',
        editNode: '编辑节点',
        editNodeName: '修改节点名',
        grantTitle: '授权（查看权限）',
        userPlaceholder: '请选择用户',
        rolePlaceholder: '请选择角色',
        grantedByServiceTree: '服务树授权：',
        grantedByServiceTreeTips: '请先在服务树里删掉节点授权',
        peopleHasRead: '当前有查看权限的人员：',
        authorizationPolicy: '实例授权策略：',
        idAuthorizationPolicy: '按节点授权的：',
        view: '查看权限',
        searchTips: '在服务树中筛选'
    },
    tree: {
        tips1: '请先到 我的订阅 页面完成订阅!',
        subSettings: '订阅设置',
    },
    topo: {
        addTopoView: '新增拓扑视图',
        editTopoView: '编辑拓扑视图',
        addTopoViewInGroup: '在分组下定义拓扑视图',
        groupRequired: '请先选择分组或者创建分组',
        viewName: '标题',
        viewNamePlaceholder: '请输入拓扑视图的标题',
        inputNameTips: '必须输入标题',
        centralNodeType: '中心节点模型',
        filterInstances: '中心节点实例',
        typeRequired: '必须要选择中心节点模型',
        instancesRequired: '实例必须要选择',
        path: '路径选择',
        aggregationCount: '聚合数',
        aggreationCountTip: '当子节点数 > 聚合数 则进行分页展示',
        preview: '预览',
        noData: '没有数据',
        edit: '编辑',
        delete: '删除',
        searchPlaceholder: '搜索拓扑视图',
        confirmDeleteView: '您确定要删除该视图吗?',
        noInstancePerm: '您没有该实例的查看权限',
        noPreferenceAttributes: '该实例没有订阅属性或者没有默认展示的属性',
        topoViewSearchPlaceholder: '请输入节点名字',
        moreBtn: '展示更多({count})'
    },
    relationSearch: {
        relationSearch: '关系搜索',
        sourceCIType: '源模型',
        sourceCITypeTip: '请输入或选择',
        sourceCITYpeInput: '请输入关键词',
        targetCIType: '目标模型',
        targetCITypeTip: '请输入或选择，可多选',
        pathSelect: '路径选择',
        pathSelectTip: '请先选择源模型和目标模型',
        saveCondition: '保存条件',
        conditionFilter: '条件过滤',
        level: '层级',
        returnPath: '返回路径',
        conditionName: '条件命名',
        path: '路径',
        expandCondition: '展开条件',
    },
    ipam: {
        overview: '概览',
        addressAssign: '地址分配',
        ipSearch: 'IP查询',
        subnetList: '子网列表',
        history: '历史记录',
        ticket: '关联工单',
        addSubnet: '新增子网',
        editSubnet: '编辑子网',
        addCatalog: '新增目录',
        editCatalog: '修改目录',
        catalogName: '目录名称',
        editName: '修改名称',
        editNode: '修改节点',
        deleteNode: '删除节点',
        basicInfo: '基本信息',
        scanRule: '扫描规则',
        adExecTarget: '执行机器',
        masterMachineTip: '安装OneMaster的所在机器',
        oneagentIdTips: '请输入以0x开头的16进制OneAgent ID',
        selectFromCMDBTips: '从CMDB中选择',
        adInterval: '采集频率',
        cronTips: '格式同crontab, 例如：0 15 * * 1-5',
        masterMachine: 'Master机器',
        specifyMachine: '指定机器',
        specifyMachineTips: '请填写指定机器！',
        cronRequiredTip: '采集频率不能为空',
        addressNullTip: '请先选择左侧子网树的叶子节点',
        addressNullTip2: '子网前缀长度必须 >= 16',
        assignedOnline: '已分配在线',
        assignedOffline: '已分配离线',
        unassignedOnline: '未分配在线',
        unused: '空闲',
        allStatus: '全部状态',
        editAssignAddress: '编辑分配地址',
        assign: '分配',
        recycle: '回收',
        assignStatus: '分配状态',
        reserved: '预留',
        assigned: '已分配',
        recycleTip: '确认要回收吗？回收后该网段状态变更为：未分配',
        recycleSuccess: '{ip} 回收成功，状态变更为: 未分配',
        operationLog: '操作记录',
        scanLog: '扫描记录',
        updateCatalog: '更新目录',
        deleteCatalog: '删除目录',
        updateSubnet: '修改子网',
        deleteSubnet: '删除子网',
        revokeAddress: '地址回收',
        operateTime: '操作时间',
        operateUser: '操作人',
        operateType: '操作类型',
        subnet: '子网',
        description: '描述',
        ipNumber: '在线IP地址数',
        startTime: '开始时间',
        endTime: '结束时间',
        scanningTime: '扫描耗时',
        viewResult: '查看结果',
        scannedIP: '已扫描的IP',
        subnetStats: '子网统计',
        addressStats: '地址数统计',
        onlineStats: '在线统计',
        assignStats: '分配统计',
        total: '总数',
        free: '空闲',
        unassigned: '未分配',
        online: '在线',
        offline: '离线',
        onlineUsageStats: '子网在线统计',
        subnetName: '子网名称',
        addressCount: '地址数',
        onlineRatio: '在线率',
        scanEnable: '是否扫描',
        lastScanTime: '最后扫描时间',
        isSuccess: '是否成功'
    }
}
export default cmdb_zh
