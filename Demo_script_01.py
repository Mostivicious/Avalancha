class FootballCrowdMaker(object):


    def __init__(self, parent=None):
        # Main widget.
        self.mainUI = QTWRAPPER.loadUi(QTWRAPPER.getModulePath(__file__))
        self.mainUI.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.mainUI.setObjectName('FootballCrowdGenerator')
        self.mainUI.move(380, 770)

        # Setting window preferences.
        self.window = QTWRAPPER.QWindow(self.mainUI)
        self.window.setWindowTitle('Football Crowd Generator')
        self.window.setFixedSize(MAINWIDTH, MAINHEIGHT)
        self.mainUI.setStyleSheet("QStatusBar{padding-left:8px;background:rgba(0,0,0,0);color:green;font-weight:bold;}")
        self.window.move(900, 100)

        # Edit widgets.
        QPixMapIcon = QPixmap(ICON)
        self.window.setWindowIcon(QIcon(QPixMapIcon))
        self.mainUI.mainProgressBarQPrb.setHidden(True)

        # Set stylesheet.
        sshFile = "P:/aronnax/maya/CDN_stylesheet.qss"
        with open(sshFile,"r") as fh:
            self.window.setStyleSheet(fh.read())

        # Init functions.
        self.functions_caller()
        self.connect_widgets()
        self.mainUI.mainLayoutQTab.setCurrentIndex(0)
        

    def functions_caller(self):
        """ Call the init functions. """
        self.create_spreed_radius_guide()
        self.resize_ui_panels()
        self.ramdomize_rotation_option()
        self.list_crowd_animation_cicles()
        self.list_particles_intances()
        self.edit_time_range_values()
        self.set_init_cache_folder()


    def connect_widgets(self):
        self.mainUI.createAgentQBttn.clicked.connect(self.generate_agents)
        self.mainUI.spreadrangeQSbx.valueChanged.connect(self.create_spreed_radius_guide)
        self.mainUI.showSpredRadiuseQRbtn.toggled.connect(self.create_spreed_radius_guide)
        self.mainUI.showSpredRadiuseQRbtn.toggled.connect(self.resize_ui_panels)
        self.mainUI.createInstancesQBttn.clicked.connect(self.generate_particles_instances)
        self.mainUI.sceneFormSetQBttn.clicked.connect(self.get_custom_shape)
        self.mainUI.createCustomMeshQBttn.clicked.connect(self.create_custom_mesh)
        self.mainUI.pointArrayCountQSbx.valueChanged.connect(self.mesh_array_node_edit)
        self.mainUI.pointSeedCountTQSbx.valueChanged.connect(self.mesh_array_node_edit)
        self.mainUI.customFormsCmb.currentIndexChanged.connect(self.mesh_array_node_type_edit)
        self.mainUI.customFormSetQBttn.clicked.connect(self.create_custom_forms)
        self.mainUI.refreshWidgetsQAct.triggered.connect(self.refresh_widgets)
        self.mainUI.selectCrowdDataNodeQAct.triggered.connect(lambda : pm.select([node for node in pm.ls(type='network') if node.__Category__.get()]))
        self.mainUI.randomizeRotationQRbtn.toggled.connect(self.ramdomize_rotation_option)
        self.mainUI.selectFocusPointQBttn.clicked.connect(self.aim_to_focus_point)
        self.mainUI.createCrowdsQBttn.clicked.connect(self.generate_crowds)
        self.mainUI.paintAgentSpreadSetQCbttn.clicked.connect(self.paint_selection_mode)
        self.mainUI.resetPaintAgentSpreadSetQBttn.clicked.connect(self.reset_current_color_paint)
        self.mainUI.visualizateAgentTypeQAct.triggered.connect(lambda  : self.agent_visualization_type(0))
        self.mainUI.visualizateCrowdsTypeQAct.triggered.connect(lambda : self.agent_visualization_type(1))
        self.mainUI.importCrowdsQAct.triggered.connect(self.import_crowds)
        self.mainUI.mainLayoutQTab.currentChanged.connect(self.resize_team_window)
        self.mainUI.changeCrowdDataQBttn.clicked.connect(self.change_crowd_team_and_gender)
        self.mainUI.exportSelectedCrowdQAct.triggered.connect(lambda : self.export_crowds('ExportSelected'))
        self.mainUI.exportAllCrowdQAct.triggered.connect(lambda : self.export_crowds('ExportAll'))        
        self.mainUI.randomCacheAnimQAct.triggered.connect(self.cache_variation)
        self.mainUI.updateCrowdQAct.triggered.connect(self.update_crowds)
        self.mainUI.removeCrowdQAct.triggered.connect(self.remove_crowd)
        self.mainUI.updateAgentsQAct.triggered.connect(self.update_agents)
        self.mainUI.genderCacheChangeCmb.currentIndexChanged.connect(self.list_crowd_animation_cicles)
        self.mainUI.updateCrowdsAnimationQBttn.clicked.connect(lambda : self.update_crowd_animation(self.mainUI.crowdsVariationQLst.currentItem()))        
        self.mainUI.randomColorVariationQAct.triggered.connect(self.random_agent_color_variation)
        self.mainUI.getMeshArrayNodeQBttn.clicked.connect(self.get_mesh_array_node)
        self.mainUI.updateParticlesListQBttn.clicked.connect(self.list_particles_intances)
        self.mainUI.setCacheFolderQBttn.clicked.connect(self.set_particle_directory)
        self.mainUI.particleInstancesQLst.itemClicked.connect(self.select_list_items)
        self.mainUI.createParticleCacheQBttn.clicked.connect(self.create_particle_cache)
        self.mainUI.createParticleCacheQBttn_2.clicked.connect(self.delete_particle_cache)
        self.mainUI.saveAnimQAct.triggered.connect(lambda : save_animation_file())
        self.mainUI.loadAnimQAct.triggered.connect(lambda : load_animation_file())
        self.mainUI.sincronizeQAct.triggered.connect(self.sincronize_agent_whit_crowds)


    def generate_agents(self):
        """ Create the agents(holders). """
        
        # Get the selected category.
        category      = self.mainUI.categoryQCmb.currentText()
        agentCrowds   = []
        offsetTimeIn  = self.mainUI.offsetTimeInQSbx.value()
        offsetTimeOut = self.mainUI.offsetTimeOutQSbx.value()

        # Checks.
        if self.mainUI.useCustomShapesQRbtn.isChecked():
            object = pm.ls(selection=True)
            if not object:
                object = self.mainUI.sceneFormQlne.text()
                if not object:
                    om.MGlobal.displayError('You have nothing selected to continue. Select something please!')
                    return
                else:
                    try:
                        object = pm.PyNode(object)
                    except Exception as error:
                        om.MGlobal.displayError(str(error))
                        return False
            else:
                object = object[0]
            
            # Star making the agent generation.
            meshToArrayNode = self.get_mesh_point_array_node(object)[0]

            # Check how many agents the user want to create.
            self.edit_progress_bar_status('Show', self.mainUI.pointArrayCountQSbx.value())
            for position in meshToArrayNode.positionArray.get():
                self.edit_progress_bar_value()
                self.mainUI.mainProgressBarQPrb.setFormat('Computing %v/%m Agents - Percentange %p %')
                if self.mainUI.categoryQCmb.currentText() == 'Random':
                    category = random.choice(['Woman', 'Man'])

                if not self.mainUI.randomizeRotationQRbtn.isChecked():
                    if self.mainUI.selectFocusPointQlne.text():
                        aimPoint = pm.PyNode(str(self.mainUI.selectFocusPointQlne.text()))
                        if pm.objExists(aimPoint):
                            self.get_category_nodes(category)
                            offsetTime = random.randint(offsetTimeIn, offsetTimeOut)
                            agent      = self.create_agent(position, [0, 0, 0], object.getScale(), category, offsetTime=offsetTime)
                            agentCrowds.append(agent)
                            self.paint_gender_color(agent.getShape(), category)
                            aimCons    = pm.aimConstraint(aimPoint, agent.getParent(), offset=[0, 0, 0], weight=1, aimVector=[0, 0, 1], upVector=[0, 1, 0], worldUpType="vector", worldUpVector=[0, 1, 0], skip=['x', 'z'])
                            if not self.mainUI.keepFocusPointQRbtn.isChecked():
                                pm.delete(aimCons)
                            continue
                        else:
                            om.MGlobal.displayError('The current selected objec as focus point is no longer exists in the scene. Try to define a new one to continue.')
                            break
                            return
                    else:
                        if self.mainUI.randomizeRotationQRbtn.isChecked():
                            YRot = random.randint(-100, 100)
                        else:
                            YRot = 0

                elif self.mainUI.randomizeRotationQRbtn.isChecked():
                    YRot = random.randint(-100, 100)
                else:
                    YRot = 0
                self.get_category_nodes(category)
                offsetTime = random.randint(offsetTimeIn, offsetTimeOut)
                agent      = self.create_agent(position, [0, YRot, 0], object.getScale(), category, offsetTime=offsetTime)
                agentCrowds.append(agent)
                self.paint_gender_color(agent.getShape(), category)                

        else:
            # Get the spreed seed.
            spreadSeed = self.mainUI.spreadrangeQSbx.value()

            # Check how many agents the user want to create.
            self.edit_progress_bar_status('Show', self.mainUI.agentsCountQSbx.value())
            agents = []            
            for number in xrange(self.mainUI.agentsCountQSbx.value()):
                self.edit_progress_bar_value()
                self.mainUI.mainProgressBarQPrb.setFormat('Computing %v/%m Agents - Percentange %p %')
                if self.mainUI.categoryQCmb.currentText() == 'Random':
                    category = random.choice(['Woman', 'Man'])
                self.get_category_nodes(category)
                posX, posY, posZ = random.randint(-spreadSeed, spreadSeed), random.randint(-spreadSeed, spreadSeed), random.randint(-spreadSeed, spreadSeed)
                rotX, rotY, rotZ = random.randint(-spreadSeed, spreadSeed), random.randint(-spreadSeed, spreadSeed), random.randint(-spreadSeed, spreadSeed)
                offsetTime = random.randint(offsetTimeIn, offsetTimeOut)
                if self.mainUI.randomizeRotationQRbtn.isChecked():
                    rotY = rotY*50
                else:
                    rotY = 0
                agent = self.create_agent([posX, 0, posZ], [0, rotY, 0], [1, 1, 1], category, offsetTime=offsetTime)
                agentCrowds.append(agent)
                self.paint_gender_color(agent.getShape(), category)
                agents.append(agent.getParent())

            posNode = pm.group(agents)
            posNode.setTranslation(pm.PyNode('__footballCrowds_painter__').getTranslation())
            for item in posNode.getChildren():
                pm.parent(item, world=True)
            pm.delete(posNode)

        # Randomize color variation.
        if self.mainUI.randomColorVariationQChk.isChecked():
            for agentControl in agentCrowds:
                agentControl.colorVariationPP.set(random.randint(1, 8))

        mc.select(clear=True)
        self.edit_progress_bar_status('Hide')


    def generate_crowds(self):
        """ Method to create the final crowds base on the current agents. """

        FootballCrowdMaker.isolate_process(mode='isolateProcessStart')
        start        = pm.timerX()
        networkNodes = [node for node in pm.ls(type='network') if hasattr(node, '__Category__')]
        currentTeam  = self.mainUI.teamSelectionCmb.currentText()
        if networkNodes:
            self.mainUI.mainProgressBarQPrb.setFormat('Computing %v/%m Crowds - Percentange %p %')
            self.edit_progress_bar_status('Show', self.mainUI.pointArrayCountQSbx.value())
            for node in networkNodes:
                for agentControl in pm.listConnections(node.__Category__, destination=True):
                    if hasattr(agentControl, 'Crowd'):
                        continue
                    crowdAsset = self.import_crowd_asset(currentTeam, node.__Category__.get())
                    self.mainUI.mainProgressBarQPrb.setFormat('Computing %v/%m - Type {} Crowd - Percentange %p %'.format(node.__Category__.get()))
                    self.edit_progress_bar_value()
                    crowdAsset.setMatrix(agentControl.getMatrix(worldSpace=True))
                    agentControl.variation.setEnums(mc.addAttr(crowdAsset.name() + '.variation', query=True, enumName=True).split(':'))
                    agentControl.variation  >> crowdAsset.variation
                    agentControl.offsetTime >> crowdAsset.offsetTime
                    bridgeNode    = pm.PyNode(crowdAsset.listConnections(type='timeToUnitConversion')[0])
                    exocortexNode = bridgeNode.listConnections(type='ExocortexAlembicTimeControl')[0]
                    agentControl.velocity >> exocortexNode.factor
                    agentControl.addAttr('Crowd', dataType='string')
                    agentControl.Crowd.set(crowdAsset.name())                    
                    agentControl.renderSet.set(crowdAsset.getChildren()[-1].listConnections(destination=True, type='objectSet'))
                    visibilityNode    = pm.createNode('choice', name=agentControl.name() + '_visibility')
                    invVisibilityNode = pm.createNode('reverse', name=agentControl.name() + '_invVisibility')
                    agentControl.VisualizationType >> visibilityNode.selector
                    visibilityNode.selector        >> invVisibilityNode.inputX
                    visibilityNode.selector        >> crowdAsset.visibility
                    invVisibilityNode.outputX      >> agentControl.getChildren()[1].visibility
                    crowdAsset.getShape().visibility.set(0)
                    pm.parentConstraint(agentControl, crowdAsset, maintainOffset=True)
                    agentControl.VisualizationType.set(1)

        mc.select(clear=True)
        FootballCrowdMaker.isolate_process(mode='isolateProcessEnd')
        self.edit_progress_bar_status('Hide')
        totalTime = pm.timerX(startTime=start)
        print "Total time: ", totalTime


    def generate_particles_instances(self):
        """ Identify and group by gender type all the current scene agents to generate the particles instances. """

        self.update_agents()
        # Checks.
        userChoice = mc.confirmDialog(title='Create particle instances',
                                          button=['Create Instances', 'Cancel'],
                                          defaultButton='Create Instances', cancelButton='Cancel',
                                          message='This action is going to convert all the current references crowds to particle instances'\
                                          ' removing the majority of the crowds and deleting all your agents. There is no way back!',
                                          dismissString='Cancel', icon='warning')

        if userChoice == 'Create Instances':
            self.plancher()
            self.sincronize_agent_whit_crowds()
            networkNodes     = self.get_network_nodes()        
            crowdsToDelete   = []
            masterControls   = []

            # Star making the gender groups dicts.
            if networkNodes:
                for node in networkNodes:
                    crowdGender = node.__Category__.get()
                    animCicles  = {}
                    for agentControl in pm.listConnections(node.__Category__, destination=True):
                        crowdAsset = [item for item in agentControl.variation.connections() if 'crowdSupporter' in item.name() and ':GEO' in item.name()]
                        if crowdAsset:
                            if mc.objExists(str(crowdAsset[0])):
                                agentControl.renderSet.set(crowdAsset[0].getChildren()[-3].listConnections(destination=True, type='objectSet'))
                                if not mc.objExists(str(agentControl.renderSet.get())):
                                    continue

                        animClips = agentControl.getAttr('variation', asString=True)

                        # First dictionary fill.
                        if crowdGender not in animCicles:
                            animCicles[crowdGender] = {agentControl.name():animClips}
                            agentControl.childrenCrowds.set(agentControl.name())
                            if not agentControl in masterControls:
                                masterControls.append(agentControl)
                        else:
                            # Check if the dictionary has allready the current anim cycle and just append the control.
                            if str(animClips) not in animCicles[crowdGender].values():
                                animCicles[crowdGender].update({agentControl.name():animClips})
                                agentControl.childrenCrowds.set(agentControl.name())
                                if not agentControl in masterControls:
                                    masterControls.append(agentControl)
                            else:
                                for key, value in animCicles[crowdGender].iteritems():
                                    if value == animClips:
                                        masterAgentControl = pm.PyNode(key)
                                        break
                                dataControl        = masterAgentControl.childrenCrowds.get()
                                if not agentControl.name() in str(dataControl):
                                    finalData = str(dataControl) + '__' +  str(agentControl.name())
                                    masterAgentControl.childrenCrowds.set(str(finalData))

                                if not masterAgentControl in masterControls:
                                    masterControls.append(masterAgentControl)
                                crowdsToDelete.append(agentControl.name())

            if len(masterControls) >= 1:
                

                # Base on the current agent nodes, start creating the instances base on category and space position.
                particleData = {}
                self.mainUI.mainProgressBarQPrb.setFormat('Computing %v/%m Instances - Percentange %p %')
                self.edit_progress_bar_status('Show', len(masterControls))
                for control in masterControls:
                    particlesPosition = []
                    aimPosition       = []
                    for agent in [pm.PyNode(item) for item in control.childrenCrowds.get().split('__')]:
                        vectorNode    = agent.worldPosition.get()
                        aimVectorNode = agent.aimPointPosition.get()
                        particlesPosition.append([vectorNode.x, vectorNode.y, vectorNode.z])
                        aimPosition.append([aimVectorNode.x, aimVectorNode.y, aimVectorNode.z])

                    # Create the particles.
                    instanceName = self.unique_name('{}_particle_instance'.format(control.name()))
                    particleSet  = self.create_crowd_particles(name=instanceName, aimVector=aimPosition, particles=particlesPosition)
                    particleSet[0].particleRenderType.set(2)
                    particleSet[0].aiExportParticleIDs.set(1)
                    rangeRGB = [[.2,.8],[.3,.6],[0,.3]]
                    agentControls = str(control.childrenCrowds.get())
                    count         = pm.nParticle(particleSet, q=1, count=1)
                    for agentControl, particleId in zip(agentControls.split('__') ,range(count)):
                        agentControl = pm.PyNode(agentControl)
                        pm.nParticle(particleSet, e=True, attribute='colorPP', id=particleId, vectorValue=(random.uniform(rangeRGB[0][0],rangeRGB[0][1]), random.uniform(rangeRGB[1][0],rangeRGB[1][1]), random.uniform(rangeRGB[2][0],rangeRGB[2][1])) )
                        pm.nParticle(particleSet, e=True, attribute='position', id=particleId, vectorValue=agentControl.worldPosition.get())
                        pm.nParticle(particleSet, e=True, attribute='position0', id=particleId, vectorValue=agentControl.worldPosition.get())
                        pm.nParticle(particleSet, e=True, attribute='aimAxisPP0', id=particleId, vectorValue=agentControl.aimAxis.get())
                        pm.nParticle(particleSet, e=True, attribute='aimAxisPP', id=particleId, vectorValue=agentControl.aimAxis.get())
                        pm.nParticle(particleSet, e=True, attribute='aimPositionPP', id=particleId, vectorValue=agentControl.aimPointPosition.get())
                        pm.nParticle(particleSet, e=True, attribute='colorVariationPP0', id=particleId, floatValue=agentControl.colorVariationPP.get())
                        pm.nParticle(particleSet, e=True, attribute='colorVariationPP', id=particleId, floatValue=agentControl.colorVariationPP.get())

                    agentParticleInstance = pm.particleInstancer(control, edit=1, name=instanceName, aimAxis=particlesPosition)
                    control.particleSet.set(particleSet[0])
                    particleData[control.renderSet.get()] = control.particleSet.get()
                    self.edit_progress_bar_value()
                    self.mainUI.mainProgressBarQPrb.setFormat('Computing {} %v/%m Instance - Percentange %p %'.format(control.name()))

                for renderSet, particleSet in particleData.iteritems():
                    self.create_instancers_for_crowds(renderSet, particleSet)

                # Delete the duplicate anim cycles crowd and just maintain.
                for item in crowdsToDelete:
                    if mc.objExists(str(item)):
                        agent = pm.PyNode(item)
                        if mc.objExists(str(agent.Crowd.get())):
                            # crowd = pm.PyNode(agent.Crowd.get())
                            # for mesh in crowd.getChildren():
                                # if mc.objExists(mesh.name()):
                                    # if 'C_body_mesh' in mesh.name():
                                        # if not mesh.matrix.listConnections():
                            pm.delete(pm.PyNode(agent.Crowd.get()).listConnections(type='parentConstraint'))
                            pm.mel.file(pm.PyNode(agent.Crowd.get()).referenceFile(), removeReference=True)

                pm.delete([pm.PyNode(item).getParent() for item in crowdsToDelete])
                
                # Delete the current agents controls and hide the current remaining reference crodws.
                controlsToDelete = []
                currentCrowds    = []
                for networkNode in self.get_network_nodes():
                    for agentControl in pm.listConnections(networkNode.__Category__, destination=True):
                        if mc.objExists(str(agentControl.Crowd.get())):
                            currentCrowds.append(agentControl.Crowd.get())
                            controlsToDelete.append(agentControl.getParent())


                pm.delete(controlsToDelete)
                for crowd in currentCrowds:
                    crowdObject = pm.PyNode(crowd)
                    namespace   = crowdObject.namespace().split(':', 1)[0]
                    mc.namespace(rename=(namespace, namespace.replace('CH', 'CR')))
                    crowdObject.visibility.set(0)
                    crowdObject.setTranslation([0, 0, 0])
                    crowdObject.setRotation([0, 0, 0])
 
                self.edit_progress_bar_status('Hide')
                mc.select(clear=True)