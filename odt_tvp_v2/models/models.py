# -*- coding: utf-8 -*-

from odoo import api, _, tools, fields, models, exceptions,  SUPERUSER_ID
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from datetime import datetime, date, time


class inheritCRM(models.Model):
	"""docstring for crmlead"""
	_inherit = 'crm.lead'

	marca = fields.Many2one('crm.marca', string='Marca', track_visibility=True)
	target = fields.Char(string='Target', track_visibility=True)
	product = fields.Char(string='Producto', track_visibility=True)
	project = fields.Many2one('project.project',string='Proyecto', track_visibility=True)
	analitica = fields.Many2one('account.analytic.account', string='Clave')
	slogan_marca = fields.Char(string='Eslogan', track_visibility=True)
	logo_marca = fields.Binary(string='Logo', track_visibility=True)
	start_date = fields.Date(string='Fecha de Arranque', track_visibility=True)
	end_date = fields.Date(string='Fecha de Cierre', track_visibility=True)

	btl = fields.Float(string='BTL/PDV',compute='_aprobado_btl', track_visibility=True)
	produccion = fields.Float(string='Producción',compute='_aprobado_produccion', track_visibility=True)
	diseño_creatividad = fields.Float(string='Diseño',compute='_aprobado_diseno', track_visibility=True)
	gestoria_logistica = fields.Float(string='Gestoria',compute='_aprobado_gestoria', track_visibility=True)
	call_center = fields.Float(string='Contact Center',compute='_aprobado_contact', track_visibility=True)
	digital = fields.Float(string='Marketing Digital',compute='_aprobado_digital',track_visibility=True)
	medios = fields.Float(string='Medios',compute='_aprobado_medios', track_visibility=True)
	logistica = fields.Float(string='Logistica', track_visibility=True)
	estrategia = fields.Float(string='Estrategia', compute='_aprobado_estrategia',track_visibility=True)
	otros_gastos = fields.Float(string='Otros',track_visibility=True)

	btl_count = fields.Integer(string='lead',compute='_compute_btl_count')
	contact_count = fields.Integer(string='lead',compute='_compute_contactcenter_count')
	produccion_count = fields.Integer(string='lead',compute='_compute_produccion_count')
	diseno_count = fields.Integer(string='lead',compute='_compute_diseno_count')
	estrategia_count = fields.Integer(string='lead',compute='_compute_estrategia_count')
	logistica_count = fields.Integer(string='lead',compute='_compute_logistica_count')
	medios_count = fields.Integer(string='lead',compute='_compute_medios_count')
	gestoria_count = fields.Integer(string='lead',compute='_compute_gestoria_count')
	digital_count = fields.Integer(string='lead',compute='_compute_digital_count')

	@api.one
	def _compute_btl_count(self):
		count1 = self.env['odt.btlpdv']
		search1 = count1.search_count([('crm_odt_id', 'in', [a.id for a in self])])
		self.btl_count = search1
	@api.one
	def _compute_produccion_count(self):
		count2 = self.env['odt.produccion']
		search2 = count2.search_count([('crm_odt_id', 'in', [a.id for a in self])])
		self.produccion_count = search2
	@api.one
	def _compute_gestoria_count(self):
		count3 = self.env['odt.gestoria']
		search3 = count3.search_count([('crm_odt_id', 'in', [a.id for a in self])])
		self.gestoria_count = search3
	@api.one
	def _compute_contactcenter_count(self):
		count4 = self.env['odt.contactcenter']
		search4 = count4.search_count([('crm_odt_id', 'in', [a.id for a in self])])
		self.contact_count = search4
	@api.one
	def _compute_logistica_count(self):
		count5 = self.env['odt.logistica']
		search5 = count5.search_count([('crm_odt_id', 'in', [a.id for a in self])])
		self.logistica_count = search5
	@api.one
	def _compute_estrategia_count(self):
		count6 = self.env['odt.estrategia']
		search6 = count6.search_count([('crm_odt_id', 'in', [a.id for a in self])])
		self.estrategia_count = search6
	@api.one
	def _compute_medios_count(self):
		count7 = self.env['odt.medios']
		search7 = count7.search_count([('crm_odt_id', 'in', [a.id for a in self])])
		self.medios_count = search7
	@api.one
	def _compute_digital_count(self):
		count8 = self.env['odt.digital']
		search8 = count8.search_count([('crm_odt_id', 'in', [a.id for a in self])])
		self.digital_count = search8
	@api.one
	def _compute_diseno_count(self):
		count9 = self.env['odt.diseno']
		search9 = count9.search_count([('crm_odt_id', 'in', [a.id for a in self])])
		self.diseno_count = search9

	@api.onchange('project')
	def _analitic_id(self):
		if self.project:
			self.analitica = self.project.analytic_account_id


	# Presupuestos autorizados
	@api.one
	@api.depends('btl','name')
	def _aprobado_btl(self):
		btl_model = self.env['odt.btlpdv']
		seach_presupuesto = btl_model.search([('crm_odt_id','=',self.name)])
		self.btl = sum(seach_presupuesto.mapped('btl'))

	@api.one
	@api.depends('produccion','name')
	def _aprobado_produccion(self):
		btl_model = self.env['odt.produccion']
		seach_presupuesto = btl_model.search([('crm_odt_id','=',self.name)])
		self.produccion = sum(seach_presupuesto.mapped('produccion'))

	@api.one
	@api.depends('medios','name')
	def _aprobado_medios(self):
		btl_model = self.env['odt.medios']
		seach_presupuesto = btl_model.search([('crm_odt_id','=',self.name)])
		self.medios = sum(seach_presupuesto.mapped('presupuesto_cliente'))

	@api.one
	@api.depends('diseño_creatividad','name')
	def _aprobado_diseno(self):
		btl_model = self.env['odt.diseno']
		seach_presupuesto = btl_model.search([('crm_odt_id','=',self.name)])
		self.diseño_creatividad = sum(seach_presupuesto.mapped('diseño_creatividad'))

	@api.one
	@api.depends('gestoria_logistica','name')
	def _aprobado_gestoria(self):
		btl_model = self.env['odt.gestoria']
		seach_presupuesto = btl_model.search([('crm_odt_id','=',self.name)])
		self.gestoria_logistica = sum(seach_presupuesto.mapped('gestoria'))

	@api.one
	@api.depends('call_center','name')
	def _aprobado_contact(self):
		btl_model = self.env['odt.contactcenter']
		seach_presupuesto = btl_model.search([('crm_odt_id','=',self.name)])
		self.call_center = sum(seach_presupuesto.mapped('contact_center'))

	@api.one
	@api.depends('digital','name')
	def _aprobado_digital(self):
		btl_model = self.env['odt.digital']
		seach_presupuesto = btl_model.search([('crm_odt_id','=',self.name)])
		self.digital = sum(seach_presupuesto.mapped('digital'))

	# @api.one
	# @api.depends('logistica','name')
	# def _aprobado_btl(self):
	# 	btl_model = self.env['odt.btlpdv']
	# 	seach_presupuesto = btl_model.search([('crm_odt_id','=',self.name)])
	# 	self.logistica = sum(seach_presupuesto.mapped('btl'))

	@api.one
	@api.depends('estrategia','name')
	def _aprobado_estrategia(self):
		btl_model = self.env['odt.estrategia']
		seach_presupuesto = btl_model.search([('crm_odt_id','=',self.name)])
		self.estrategia = sum(seach_presupuesto.mapped('estrategia'))

	rp_1 = fields.Char(string='¿Para que estamos haciendo este proyecto y cual es el reto?', track_visibility=True)
	rp_2 = fields.Char(string='¿Que queremos que se sepa y sienta la gente sobre el proeycto?', track_visibility=True)
	rp_3 = fields.Char(string='¿Que buscamos lograr?', track_visibility=True)
	rp_4 = fields.Char(string='¿Cual es el problema a resolver?', track_visibility=True)
	on_1 = fields.Char(string='¿Crecimiento?', track_visibility=True)
	on_2 = fields.Char(string='¿Mayor margen de utilidad?', track_visibility=True)
	on_3 = fields.Char(string='¿Posicionamiento de un nuevo producto o servicio?', track_visibility=True)
	on_4 = fields.Char(string='¿Hacer frente a la competencia?', track_visibility=True)
	ob_1 = fields.Char(string='¿Conocimiento?', track_visibility=True)
	ob_2 = fields.Char(string='¿Posicionamiento?', track_visibility=True)
	ob_3 = fields.Char(string='¿Diferenciacion?', track_visibility=True)
	cm_1 = fields.Char(string='¿Como se define y posiciona la marca en cuanto a si misma?', track_visibility=True)
	cm_2 = fields.Char(string='¿Que linea de comunicación esta implementando la marca actualmente?', track_visibility=True)
	cm_3 = fields.Char(string='¿Descripcion de la marca (Joven, solida, dinamica, innovadora, flexible, segura, institucional, preocupada por el consumidor)?', track_visibility=True)
	cm_4 = fields.Char(string='¿Que tono se debe adoptar?', track_visibility=True)
	qcs_1 = fields.Char(string='¿Quiénes son los competidores?', track_visibility=True)
	qcs_2 = fields.Char(string='¿En qué se diferencia la marca ante la competencia (beneficios al consumidor)?', track_visibility=True)
	qcs_3 = fields.Char(string='¿Qué piensan y sienten los consumidores acerca de la competencia?', track_visibility=True)
	vh_1 = fields.Char(string='¿NSE, TARGET?', track_visibility=True)
	vh_2 = fields.Char(string='¿Cuál es el comportamiengo habitual?', track_visibility=True)
	vh_3 = fields.Char(string='¿Qué piensan y sienten acerca de la marca?', track_visibility=True)
	dc_1 = fields.Char(string='7. ¿QUÉ DEBEMOS COMUNICAR?', track_visibility=True)
	dc_2 = fields.Char(string='¿Qué queremos que piensen y sientan de la marca?', track_visibility=True)
	dc_3 = fields.Char(string='¿Qué queremos que se sepa y sienta la gente sobre esta comunicación?', track_visibility=True)
	qc_1 = fields.Char(string='8. ¿QUÉ NO QUEREMOS COMUNICAR?', track_visibility=True)
	qc_2 = fields.Char(string='9. ¿CÓMO SE COMPORTA EL CONSUMIDOR RESPECTO AL PRODUCTO O SERVICIO ACTUALMENTE (CONDUCTAS Y CARENCIAS)?', track_visibility=True)
	ccp_1 = fields.Char(string='10. ¿QUÉ OTRAS PROMOCIONES HA TENIDO LA MARCA?', track_visibility=True)
	ccp_2 = fields.Char(string='¿Qué resultados obtuvieron?', track_visibility=True)
	cdp_1 = fields.Char(string='¿Qué medios se utilizarán para la implementación?', track_visibility=True)
	cdp_2 = fields.Char(string='¿Qué medios se utilizarán para la difusión?', track_visibility=True)
	cdp_3 = fields.Char(string='¿Qué medios se utilizarán para la participación?', track_visibility=True)
	qz_12 = fields.Char(string='¿CUÁL ES EL MARCO LEGAL?(RTC, SEGOB, PROFECO, MICROSITIOS Y PROMOWEB)', track_visibility=True)
	qz_13 = fields.Char(string='¿HAY REQUERIMIENTO ADICIONALES? /n Medios de datos y consideraciones creativas, mandatorios con respecto al uso de la marca, aspectos legales, manejo de los modulos,etc', track_visibility=True)
	qz_14 = fields.Char(string='¿HAY UN ESTIMADO DE PRESUPUESTO?', track_visibility=True)
	qz_15 = fields.Char(string='¿CUÁLES SON LOS ENTREGABLES?', track_visibility=True)
	qz_16 = fields.Char(string='¿SE TRABAJARA EN CONJUNCO CON ALGUNA AGENCIA DE LA MARCA?', track_visibility=True)
		
class CrmOdt(models.Model):
	_name = 'crm.odt'
	_description = 'Campos del crm que se muestran en todas las ventanas de las areas para las diferentes ODTs'


	def _default_probability(self):
		stage_id = self._default_stage_id()
		if stage_id:
			return self.env['crm.stage'].browse(stage_id).probability
		return 10

	def _default_stage_id(self):
		team = self.env['crm.team'].sudo()._get_default_team_id(user_id=self.env.uid)
		return self._stage_find(team_id=team.id, domain=[('fold', '=', False)]).id



	project_name = fields.Char(string='Nombre del proyecto')
	crm_odt_id = fields.Many2one('crm.lead', 'Oportunidad')
	name = fields.Char(string='Nombre', default=lambda *a: 'Nuevo', readonly=True)
	tag_ids = fields.Many2many('crm.lead.tag', 'crm_lead_tag_rel', 'lead_id', 'tag_id',related='crm_odt_id.tag_ids', string='Tags', help="Classify and analyze your lead/opportunity categories like: Training, Service")
	stage_id = fields.Many2one('crm.stage', string='Stage', ondelete='restrict', track_visibility='onchange', index=True,
		domain="['|', ('team_id', '=', False), ('team_id', '=', team_id)]",
		group_expand='_read_group_stage_ids', default=lambda self: self._default_stage_id())
	team_id = fields.Many2one('crm.team',related='crm_odt_id.team_id', string='Sales Team', oldname='section_id', default=lambda self: self.env['crm.team'].sudo()._get_default_team_id(user_id=self.env.uid),
		index=True, track_visibility='onchange', help='When sending mails, the default email address is taken from the Sales Team.')
	kanban_state = fields.Selection([('normal','In Progress'),('blocked','Blocked'),('done','Ready for next Stage')], 'Kanban State', default='normal')
	user_id = fields.Many2one('res.users', related='crm_odt_id.user_id',string='Salesperson', index=True, track_visibility='onchange', default=lambda self: self.env.user)
	partner_id = fields.Many2one('res.partner',related='crm_odt_id.partner_id', string='Customer', track_visibility='onchange', track_sequence=1, index=True,
				help="Linked partner (optional). Usually created when converting the lead. You can find a partner by its Name, TIN, Email or Internal Reference.")
	priority = fields.Selection([('0','Low'),('1','Normal'),('2','High'),('3','Very High')],related='crm_odt_id.priority',string='Priority', default='1')
	color = fields.Integer(related='crm_odt_id.color',string='Color Index')
	active = fields.Boolean(related='crm_odt_id.active',string='Active', default=True, track_visibility=True)
	email_from = fields.Char('Email', help="Email address of the contact", track_visibility='onchange', track_sequence=4, index=True)
	partner_address_email = fields.Char(related='crm_odt_id.partner_address_email',string='Partner Contact Email', readonly=True)
	partner_address_phone = fields.Char(related='crm_odt_id.partner_address_phone',string='Partner Contact Phone', readonly=True)
	date_deadline = fields.Date(related='crm_odt_id.date_deadline',string='Expected Closing', help="Estimate of the date on which the opportunity will be won.")
	partner_name = fields.Char(related='crm_odt_id.partner_name',string='Customer Name')
	date_conversion = fields.Datetime(related='crm_odt_id.date_conversion',string='Conversion Date', readonly=True)
	description = fields.Text(related='crm_odt_id.description',string='Notes', track_visibility='onchange', track_sequence=6)
	contact_name = fields.Char(related='crm_odt_id.contact_name',string='Contact Name', track_visibility='onchange', track_sequence=3)
	day_close = fields.Float(related='crm_odt_id.day_close',string='Days to Close', store=True)
	day_open = fields.Float(related='crm_odt_id.day_open',string='Days to Assign', store=True)
	referred = fields.Char(related='crm_odt_id.referred',string='Referred By')
	type = fields.Selection([('lead', 'Lead'), ('opportunity', 'Opportunity')],related='crm_odt_id.type',string='type', index=True, help="Type is used to separate Leads and Opportunities")
	campaign_id = fields.Many2one(related='crm_odt_id.campaign_id',string='Campaing')
	medium_id = fields.Many2one(related='crm_odt_id.medium_id',string='Medium')
	source_id = fields.Many2one(related='crm_odt_id.source_id',string='Source')
	street = fields.Char(related='crm_odt_id.street',string='Street')
	street2 = fields.Char(related='crm_odt_id.street2',string='Street2')
	zip = fields.Char(related='crm_odt_id.zip',string='Zip', change_default=True)
	city = fields.Char(related='crm_odt_id.city',string='City')
	state_id = fields.Many2one("res.country.state",related='crm_odt_id.state_id', string='State')
	country_id = fields.Many2one('res.country',related='crm_odt_id.country_id', string='Country')
	phone = fields.Char(related='crm_odt_id.phone',string='Phone', track_visibility='onchange', track_sequence=5)
	mobile = fields.Char(related='crm_odt_id.mobile',string='Mobile')
	function = fields.Char(related='crm_odt_id.function',string='Job Position')
	title = fields.Many2one('res.partner.title',related='crm_odt_id.title')
	company_id = fields.Many2one('res.company',related='crm_odt_id.company_id', string='Company', index=True, default=lambda self: self.env.user.company_id.id)
	lost_reason = fields.Many2one('crm.lost.reason',related='crm_odt_id.lost_reason', string='Lost Reason', index=True, track_visibility='onchange')
	partner_is_blacklisted = fields.Boolean(related='crm_odt_id.partner_is_blacklisted',string='Partner is blacklisted', readonly=True)
	is_blacklisted = fields.Boolean(related='crm_odt_id.is_blacklisted')
	marca = fields.Many2one('crm.marca', related='crm_odt_id.marca',string='Marca')
	target = fields.Char(string='Target')
	start_date = fields.Date(related='crm_odt_id.start_date',string='Fecha de Arranque')
	end_date = fields.Date(related='crm_odt_id.end_date',string='Fecha de Cierre')

	# BRIEF
	rp_1 = fields.Char(related='crm_odt_id.rp_1',string='¿Para que estamos haciendo este proyecto y cual es el reto?')
	rp_2 = fields.Char(related='crm_odt_id.rp_2',string='¿Que queremos que se sepa y sienta la gente sobre el proeycto?')
	rp_3 = fields.Char(related='crm_odt_id.rp_3',string='¿Que buscamos lograr?')
	rp_4 = fields.Char(related='crm_odt_id.rp_4',string='¿Cual es el problema a resolver?')
	on_1 = fields.Char(related='crm_odt_id.on_1',string='¿Crecimiento?')
	on_2 = fields.Char(related='crm_odt_id.on_2',string='¿Mayor margen de utilidad?')
	on_3 = fields.Char(related='crm_odt_id.on_3',string='¿Posicionamiento de un nuevo producto o servicio?')
	on_4 = fields.Char(related='crm_odt_id.on_4',string='¿Hacer frente a la competencia?')
	ob_1 = fields.Char(related='crm_odt_id.ob_1',string='¿Conocimiento?')
	ob_2 = fields.Char(related='crm_odt_id.ob_2',string='¿Posicionamiento?')
	ob_3 = fields.Char(related='crm_odt_id.ob_3',string='¿Diferenciacion?')
	cm_1 = fields.Char(related='crm_odt_id.cm_1',string='¿Como se define y posiciona la marca en cuanto a si misma?')
	cm_2 = fields.Char(related='crm_odt_id.cm_2',string='¿Que linea de comunicación esta implementando la marca actualmente?')
	cm_3 = fields.Char(related='crm_odt_id.cm_3',string='¿Descripcion de la marca (Joven, solida, dinamica, innovadora, flexible, segura, institucional, preocupada por el consumidor)?')
	cm_4 = fields.Char(related='crm_odt_id.cm_4',string='¿Que tono se debe adoptar?')
	qcs_1 = fields.Char(related='crm_odt_id.qcs_1',string='¿Quiénes son los competidores?')
	qcs_2 = fields.Char(related='crm_odt_id.qcs_2',string='¿En qué se diferencia la marca ante la competencia (beneficios al consumidor)?')
	qcs_3 = fields.Char(related='crm_odt_id.qcs_3',string='¿Qué piensan y sienten los consumidores acerca de la competencia?')
	vh_1 = fields.Char(related='crm_odt_id.vh_1',string='¿NSE, TARGET?')
	vh_2 = fields.Char(related='crm_odt_id.vh_2',string='¿Cuál es el comportamiengo habitual?')
	vh_3 = fields.Char(related='crm_odt_id.vh_3',string='¿Qué piensan y sienten acerca de la marca?')
	dc_1 = fields.Char(related='crm_odt_id.dc_1',string='7. ¿QUÉ DEBEMOS COMUNICAR?')
	dc_2 = fields.Char(related='crm_odt_id.dc_2',string='¿Qué queremos que piensen y sientan de la marca?')
	dc_3 = fields.Char(related='crm_odt_id.dc_3',string='¿Qué queremos que se sepa y sienta la gente sobre esta comunicación?')
	qc_1 = fields.Char(related='crm_odt_id.qc_1',string='8. ¿QUÉ NO QUEREMOS COMUNICAR?')
	qc_2 = fields.Char(related='crm_odt_id.qc_2',string='9. ¿CÓMO SE COMPORTA EL CONSUMIDOR RESPECTO AL PRODUCTO O SERVICIO ACTUALMENTE (CONDUCTAS Y CARENCIAS)?')
	ccp_1 = fields.Char(related='crm_odt_id.ccp_1',string='10. ¿QUÉ OTRAS PROMOCIONES HA TENIDO LA MARCA?')
	ccp_2 = fields.Char(related='crm_odt_id.ccp_2',string='¿Qué resultados obtuvieron?')
	cdp_1 = fields.Char(related='crm_odt_id.cdp_1',string='¿Qué medios se utilizarán para la implementación?')
	cdp_2 = fields.Char(related='crm_odt_id.cdp_2',string='¿Qué medios se utilizarán para la difusión?')
	cdp_3 = fields.Char(related='crm_odt_id.cdp_3',string='¿Qué medios se utilizarán para la participación?')
	qz_12 = fields.Char(related='crm_odt_id.qz_12',string='¿CUÁL ES EL MARCO LEGAL?(RTC, SEGOB, PROFECO, MICROSITIOS Y PROMOWEB)')
	qz_13 = fields.Char(related='crm_odt_id.qz_13',string='¿HAY REQUERIMIENTO ADICIONALES? /n Medios de datos y consideraciones creativas, mandatorios con respecto al uso de la marca, aspectos legales, manejo de los modulos,etc')
	qz_14 = fields.Char(related='crm_odt_id.qz_14',string='¿HAY UN ESTIMADO DE PRESUPUESTO?')
	qz_15 = fields.Char(related='crm_odt_id.qz_15',string='¿CUÁLES SON LOS ENTREGABLES?')
	qz_16 = fields.Char(related='crm_odt_id.qz_16',string='¿SE TRABAJARA EN CONJUNCO CON ALGUNA AGENCIA DE LA MARCA?')
	product = fields.Char(related='crm_odt_id.product',string='Producto', track_visibility=True)
	project = fields.Many2one('project.project',related='crm_odt_id.project',string='Proyecto', track_visibility=True)
	analitica = fields.Many2one('account.analytic.account',related='crm_odt_id.analitica',string='Clave')
	slogan_marca = fields.Char(related='crm_odt_id.slogan_marca',string='Eslogan', track_visibility=True)
	logo_marca = fields.Binary(related='crm_odt_id.logo_marca',string='Logo', track_visibility=True)
	personal = fields.Char(string='Personal', track_visibility=True)
	propiedad = fields.Char(string='PROPIEDAD:', track_visibility=True)
	descrption = fields.Text(string='Descrpicion', track_visibility=True)


	@api.model
	def _read_group_stage_ids(self, stages, domain, order):

		team_id = self._context.get('default_team_id')
		if team_id:
			search_domain = ['|', ('id', 'in', stages.ids), '|', ('team_id', '=', False), ('team_id', '=', team_id)]
		else:
			search_domain = ['|', ('id', 'in', stages.ids), ('team_id', '=', False)]

		# perform search
		stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
		return stages.browse(stage_ids)

	def _stage_find(self, team_id=False, domain=None, order='sequence'):
		""" Determine the stage of the current lead with its teams, the given domain and the given team_id
			:param team_id
			:param domain : base search domain for stage
			:returns crm.stage recordset
		"""
		# collect all team_ids by adding given one, and the ones related to the current leads
		team_ids = set()
		if team_id:
			team_ids.add(team_id)
		for lead in self:
			if lead.team_id:
				team_ids.add(lead.team_id.id)
		# generate the domain
		if team_ids:
			search_domain = ['|', ('team_id', '=', False), ('team_id', 'in', list(team_ids))]
		else:
			search_domain = [('team_id', '=', False)]
		# AND with the domain in parameter
		if domain:
			search_domain += list(domain)
		# perform search, return the first found
		return self.env['crm.stage'].search(search_domain, order=order, limit=1)

class OdtMedios(models.Model):
	_name = 'odt.medios'
	_description = 'Ventana kanban para la estructura de medios'
	_inherit = ['mail.thread', 'mail.activity.mixin','crm.odt']

	presupuesto_cliente = fields.Float(string='Presupuesto del Cliente', track_visibility=True)
	med_tipo_trabajo = fields.Selection([('1','Revisión de Pauta'),('2','Análisis'),('3','Plan de Medios')], string='Tipo de Trabajo Requerido', track_visibility=True)
	# sección para odt medios
	med_spot_tv_abierta = fields.Boolean(string='Spot TV Abierta TVSA', track_visibility=True)
	med_aaee_tv = fields.Boolean(string='AAEE TV TVSA', track_visibility=True)
	med_brief_aaee = fields.Boolean(string='Brief AAEE', track_visibility=True)
	med_spoteo_carriers = fields.Boolean(string='Spoteo Carriers', track_visibility=True)
	med_net_televisa = fields.Boolean(string='Networks Televisa', track_visibility=True)
	med_otros_net = fields.Boolean(string='Otros Networks', track_visibility=True)
	med_radio = fields.Boolean(string='Radio', track_visibility=True)
	med_revista = fields.Boolean(string='Revista', track_visibility=True)
	med_prensa = fields.Boolean(string='Prensa', track_visibility=True)
	med_ooh = fields.Boolean(string='OOH', track_visibility=True)
	med_digital = fields.Boolean(string='Digital', track_visibility=True)
	med_analisis = fields.Boolean(string='Análisis', track_visibility=True)

	#	Medios
	med_folio = fields.Char(string='Folio', track_visibility=True)
	med_fecha_soli = fields.Datetime(string='Fecha de solicitud', track_visibility=True)
	med_hora_soli = fields.Datetime(string='Hora de Solicitud', track_visibility=True)
	med_fecha_entrega = fields.Datetime(string='Fecha Estimada de Entrega', track_visibility=True)
	med_fecha_real = fields.Datetime(string='Fecha Real de Entrega', track_visibility=True)
	med_elabora = fields.Char(string='Elaborará este Plan', track_visibility=True)
	med_nivel_complejidad = fields.Char(string='Nivel de complejidad', track_visibility=True)

	# odt medios
	med_odt_fecha_entrega = fields.Datetime(string='Fecha de entrega solicitada', track_visibility=True)
	#med_clave_proyecto = fields.Char(string='Clave de Proyecto', track_visibility=True)
	# Plan de medios
	med_objetivo_comunicacion = fields.Char(string='Objetivo de comunicación', track_visibility=True)
	med_presupuesto_cliente = fields.Char(string='Presupuesto Global Cliente', track_visibility=True)
	med_periodo_camap = fields.Char(string='Periodo campaña y/o promoción', track_visibility=True)
	med_tipo_analisis = fields.Selection([('1','Inversión Publicitaria (Competencia)'),('2','Audiencia (Ratings)'),('3','Hábitos de Consumo (BIMSA)')],string='Tipo de Análisis', track_visibility=True)
	med_oberv_generales = fields.Text(string='Observaciones Generales', track_visibility=True)
	med_solicita = fields.Char(string='Nombre de quien solicita', track_visibility=True)
	med_getente = fields.Char(string='Gerente Medios', track_visibility=True)
	med_dirc_comercial = fields.Char(string='Dirección Comercial', track_visibility=True)
	med_icepresidencia = fields.Char(string='Vicepresidencia', track_visibility=True)

	#Solicitud TVSA
	tvsa_tipo_camp = fields.Selection([('1','TEASER'),('2','LANZAMIENTO'),('3','REGULAR')],string='Tipo de Campaña', track_visibility=True)
	tvsa_otro = fields.Char(string='Otro: (Especificar)')
	tvsa_catego_televisa = fields.Selection([('1','02SG-Algodon/Cotonetes'),('2','00AE-Alimentos en lata e instanta'),('3','00AI-Alimentos infantiles'),
                    ('4','00WB-Alimentos/art p animales'),('5','00CA-Almacen/mueble/Tdepartame'),('6','00JE-Anteojos/lentes de contacto '),
                    ('7','SG04-Antiacidos'),('8','04SG-Anticonceptivos/preservativos'),('9','SG09-Antigripal '),('10','00SH-Aparatos p la salud'),
                    ('11','00IA-Aparatos/acces de video'),('12','00IB-Aparatos/acces sonido'),('13','00LA-Art de limpieza en grl'),('14','00DA-Art deportivo/campamentos'),('15','00TA-Art/acces pcfumar /dejar de'),('16','00NA-Auromóviles/Automotores'),('17','00SG-Bandita/tela adhesiva/venda'),
                    ('18','01VA-Barnices/lacas/pinturas inter'),('19','01AO-Barras Alimenticias'),('20','00BB-Bebidas alcohólicas'),('21','02BA-Bebidas Isotonicas'),
                    ('22','00SC-Biberones/cosmet bebe'),('23','00RD-Blancos'),('24','00LD-Bolsas/plasticos desechables'),('25','00AC-Botanas'),('26','00AB-Cafes/tes/mod de leche'),('27','00RC-Calzado'),('28','00HA-Camp Civicas/org no guber'),('29','02VA-Candados/cerrad protección'),('30','00AH-Carnes frias'),('31','00AM-Carnes/prod animales'),('32','03CA-Centros comerciales'),('33','02LA-Ceras'),
                    ('34','00AO-Cereales'),('35','01BB-Cerveza/bedib baja graduación'),('36','00AK-Chocolates/dulces/caramelos'),('37','03HB-Clinicas de belleza/estetica'),('38','01EC-Colchones'),('39','00NH-Combustib/lubricant auto'),('40','00PA-Computación'),('41','01KD-Congresos/simpos/conferenc'),('42','01AN-Consomes'),('43','00VB-Construcción y Vialidad'),('44','09SH-ConsumoResposable Alcohol'),('45','00SE-Cosmetico/maquill/desmaq'),('46','00SJ-Cremas/protectores p piel'),
                    ('47','01DB-Ctro de enteten/zoo/bal'),('48','04HB-Cupones/vales de despensa'),('49','00EE-Decoración/adornos hogar'),('50','002SE-Depiladores'),('51','02DB-Deportivos/gimnasios'),('52','02SB-Desodorantes/antitranspirantes')
                    ,('53','03LA-Destapacanos/desasolvadores'),('54','00LC-Detergentes/jabon p ropa'),('55','00IC-Discos/cassettes/compactos'),('56','01EB-Economizad/Purificad agua'),('57','00AJ-Edulcorante'),('58','00EA-Electrodomest/línea blanca'),('59','00XA-Equipo p oficina o escuela'),('60','00VC-Equipos industriales'),('61','00KA-Escuelas/Institutos/Cursos'),('62','02KD-Espectaculos/Teatro/Circo')
                    ,('63','03SB-Esponjas limpiad p piel'),('64','06CA-Farmacias'),('65','05CA-Ferreterias'),('66','00SA-Fijadores/tratam p cabello'),('67','00ID-Fotografia'),('68','00SI-Fragancias'),('69','00AF-Frutas nat/legum/verduras'),('70','05AG-Funerarias,Velatorios'),('71','03KD-Galerias/expos/ferias/museos'),('72','01HA-Gobierno/camp gubernamental')
                    ,('73','00AS-Harinas/Tortillas/tostadas'),('74','00VE-Herramientas'),('75','01AM-Hielo'),('76','00SF-Higiene intima femenina'),('77','00OA-Hoteles'),('78','00ED-Iluminacion/pilas/focos/velas'),('79','03VA-Impermeabilizantes'),('80','00VD-Inmobiliarias'),('81','00LB-Insecticidas'),('82','00JA-Instrumentos/acc musicales')
                    ,('83','04SB-Jabon toc/shampoos piel'),('84','EA15-Jabon Lavatrastes'),('85','00JB-Juegos/juguetes'),('86','03BA-Jugos/nectares'),('87','SG15-Laxantes'),('88','00AG-Leches'),('89','00KC-Libros/revistas/Med impresos'),('90','00UA-Loterias/juegos de azar'),('91','01JE-Maletas/bolsas/portafolios'),('92','01AG-Mantequillas/margarinas')
                    ,('93','00MA-Maquinas/refacciones'),('94','04VA-Materiales p construcción'),('95','03SG-Medicamentos en General'),('96','00NB-Motocicletas'),('97','08SB-Pañales desechables'),('98','01LD-Palillos'),('99','00AA-Panificacion'),('100','02LD-Papel aluminio/encerado'),('101','06SB-Papel/pañuelo/servill desech'),
                     ('102','02HA-Partidos politicos'),('103','05KD-Peliculas/cines'),('104','05VA-Pisos/losetas/azulejos'),('105','02EB-Plateria general'),('106','03LD-Platos/vasos/cubiert desecha'),('107','00AP-Postres/mermelad/helados'),('108','00SD-Prod p higiene bucal'),('109','06SG-Productos contra el acné'),('110','07SB-Productos ortopédicos'),('111','05SG-Pruebas de embarazo'),('112','06VA-Puertas eléctricas/general')
                    ,('113','00PF-Pulpa de fruta'),('114','02AN-Pures'),('115','02AG-Quesos'),('116','01KB-Radio'),('117','00BA-Refrescos'),('118','00JF-Relojes/joyas'),('119','00OB-Restaurant/Gastron/Cnocturno'),('120','00RB-Ropa'),('121','03AN-Salsas'),('122','00FB-Seguros'),('123','05HB-Serv mensajería/paquetería'),('124','00FA-Serv. bancarios/financieros'),('125','02HB-Servicios de Salud'),('126','01SA-Shampoos/acondicionadores'),('127','03KB-Sist de televisión paga'),('128','00AD-Sopas'),('129','LC04-Suavizantes de ropa'),('130','03AG-Sustitutos de crema'),('131','00RA-Telas/hilos/acce p cost'),('132','00QA-Telecomunicaciones')
                    ,('133','00QB-Telefonia Celular'),('134','00CD-Telemercadeo'),('135','04CA-Tienda disco/cassette/video'),('136','01CA-Tiendas de autoservicio'),('137','03SA-Tintes p cabello'),('138','03SC-Toallas húmedas'),('139','08SG-Tratam p adelgazar'),('140','00OC-Turismo/viajes/Líneas aéreas'),('141','00OC-Turismo/viajes/Líneas aéreas'),('142','0001-Uso Interno Espacio Garantizad')
                    ,('143','00PT-Uso Interno Patrocinio'),('144','0003-Uso Interno Promoción'),('145','02KB-Uso Interno Promoción canal tv'),('146','00EB-Utensilios de cocina'),('147','08VA-Ventanas/vidrios/closets'),('148','09SB-Vigor sexual'),('149','09SG-Vitamina/complemen aliment'),('150','04AG-Yoghurts')], string='Categoría Televisa', track_visibility=True)

	tvsa_nse = fields.Selection([('1','ABC+ Alto + Medio alto'),('2','C Medio'),('3','D+ Medio Bajo'),('4','DE Bajo')], string="NSE", track_visibility=True)

	tvsa_grupo_edad_1 = fields.Boolean(string='4 - 12', track_visibility=True)
	tvsa_grupo_edad_2 = fields.Boolean(string='13 - 18', track_visibility=True)
	tvsa_grupo_edad_3 = fields.Boolean(string='19 - 29', track_visibility=True)
	tvsa_grupo_edad_4 = fields.Boolean(string='30 - 44', track_visibility=True)
	tvsa_grupo_edad_5 = fields.Boolean(string='45 - 54', track_visibility=True)
	tvsa_grupo_edad_6 = fields.Boolean(string='55+', track_visibility=True)
	tvsa_grupo_edad_otro = fields.Char(string='Otro', track_visibility=True)
	tvsa_sexo_p = fields.Boolean(string='Personas', track_visibility=True)
	tvsa_sexo_m = fields.Boolean(string='Mujeres', track_visibility=True)
	tvsa_sexo_h = fields.Boolean(string='Hombres', track_visibility=True)
	tvsa_rol_family = fields.Selection([('1','Jefes de Familia'),('2','Amas de Casa'),('3','Responsables de niños')],string='Rol Familiar', track_visibility=True)
	years_03 = fields.Boolean(string='0 a 3 años', track_visibility=True)
	years_48 = fields.Boolean(string='4 a 8 años', track_visibility=True)
	years_912 = fields.Boolean(string='9 a 12 años', track_visibility=True)
	target_secundario = fields.Char(string='Target Secundario', track_visibility=True)

	duracion_spot = fields.Selection([('1','10"'),('2','20"'),('3','30"'),('4','40"'),('5','50"'),('6','60"')], string='Duración de spot', track_visibility=True)
	opcion_compra = fields.Selection([('1','CPR MODULOS'),('2','CPR FRANJAS'),('3','MIXTO MÓDULO Y FRANJA'),('4','CPR POR PROGRAMA'),('5','SPOTEO')],string='Opciones de Compra', track_visibility=True)
	mixto_proporcion = fields.Char(string='En caso de ser Mixto especificar proporción', track_visibility=True)
	target_compra_modulo = fields.Char(string='Target de compra Módulos o Franja', track_visibility=True)
	target_especial = fields.Char(string='En caso de ser Target de compra Especial, Especificar', track_visibility=True)

	#regulación
	cofepris = fields.Selection([('1','SI'),('2','NO')],string='COFEPRIS', track_visibility=True)
	a_favor = fields.Selection([('1','SI'),('2','NO')],string='A favor de lo mejor', track_visibility=True)
	kids_policy = fields.Selection([('1','SI'),('2','NO')],string='Kids Policy', track_visibility=True)
	sptv_periodo_camp1 = fields.Char(string='Periodo de la Campaña', track_visibility=True)
	cpr_modulos = fields.Selection([('1','SI'),('2','NO')],string='CPR', track_visibility=True)
	canal_1 = fields.Boolean(string='2', track_visibility=True)
	canal_2 =  fields.Boolean(string='5', track_visibility=True)
	canal_3 =  fields.Boolean(string='9', track_visibility=True)
	tvsa_abierta = fields.Integer(string='Monto Máximo Inversión TV Abierta Nacional (Costo Cliente)', track_visibility=True)
	tv_abierta_duracion_spot = fields.Char(string='Duración del Spot', track_visibility=True)

	canal_local = fields.Boolean(string='Canal Local', track_visibility=True)
	bloqueos = fields.Boolean(string='Bloqueos', track_visibility=True)
	sptv_periodo_camp2 = fields.Char(string='Periodo de la Campaña', track_visibility=True)
	foro_tv = fields.Boolean(string='Foro TV', track_visibility=True)
	foro_tv_descrip = fields.Text(string='Box', track_visibility=True)
	monto_inverison_tvabierta = fields.Float(string='Monto Máximo Inversión TV Abierta Local (Costo Cliente)', track_visibility=True)
	asignacion_a = fields.Char(string='Asignado a', track_visibility=True)
	tvsa_abierta_observaciones = fields.Text(string='Observaciones generales o condiciones especiales', track_visibility=True)

	# AAEETV
	aaee_categoria_televisa = fields.Selection([('1','02SG-Algodon/Cotonetes'),('2','00AE-Alimentos en lata e instanta'),('3','00AI-Alimentos infantiles'),
                    ('4','00WB-Alimentos/art p animales'),('5','00CA-Almacen/mueble/Tdepartame'),('6','00JE-Anteojos/lentes de contacto '),
                    ('7','SG04-Antiacidos'),('8','04SG-Anticonceptivos/preservativos'),('9','SG09-Antigripal '),('10','00SH-Aparatos p la salud'),
                    ('11','00IA-Aparatos/acces de video'),('12','00IB-Aparatos/acces sonido'),('13','00LA-Art de limpieza en grl'),('14','00DA-Art deportivo/campamentos'),('15','00TA-Art/acces pcfumar /dejar de'),('16','00NA-Auromóviles/Automotores'),('17','00SG-Bandita/tela adhesiva/venda'),
                    ('18','01VA-Barnices/lacas/pinturas inter'),('19','01AO-Barras Alimenticias'),('20','00BB-Bebidas alcohólicas'),('21','02BA-Bebidas Isotónicas'),
                    ('22','00SC-Biberones/cosmet bebe'),('23','00RD-Blancos'),('24','00LD-Bolsas/plásticos desechables'),('25','00AC-Botanas'),('26','00AB-Cafes/tes/mod de leche'),('27','00RC-Calzado'),('28','00HA-Camp Civicas/org no guber'),('29','02VA-Candados/cerrad protección'),('30','00AH-Carnes frías'),('31','00AM-Carnes/prod animales'),('32','03CA-Centros comerciales'),('33','02LA-Ceras'),
                    ('34','00AO-Cereales'),('35','01BB-Cerveza/bedib baja graduación'),('36','00AK-Chocolates/dulces/caramelos'),('37','03HB-Clinicas de belleza/estetica'),('38','01EC-Colchones'),('39','00NH-Combustib/lubricant auto'),('40','00PA-Computación'),('41','01KD-Congresos/simpos/conferenc'),('42','01AN-Consomes'),('43','00VB-Construcción y Vialidad'),('44','09SH-ConsumoResposable Alcohol'),('45','00SE-Cosmetico/maquill/desmaq'),('46','00SJ-Cremas/protectores p piel'),
                    ('47','01DB-Ctro de enteten/zoo/bal'),('48','04HB-Cupones/vales de despensa'),('49','00EE-Decoración/adornos hogar'),('50','002SE-Depiladores'),('51','02DB-Deportivos/gimnasios'),('52','02SB-Desodorantes/antitranspirantes')
                    ,('53','03LA-Destapacanos/desasolvadores'),('54','00LC-Detergentes/jabon p ropa'),('55','00IC-Discos/cassettes/compactos'),('56','01EB-Economizad/Purificad agua'),('57','00AJ-Edulcorante'),('58','00EA-Electrodomest/línea blanca'),('59','00XA-Equipo p oficina o escuela'),('60','00VC-Equipos industriales'),('61','00KA-Escuelas/Institutos/Cursos'),('62','02KD-Espectaculos/Teatro/Circo')
                    ,('63','03SB-Esponjas limpiad p piel'),('64','06CA-Farmacias'),('65','05CA-Ferreterias'),('66','00SA-Fijadores/tratam p cabello'),('67','00ID-Fotografia'),('68','00SI-Fragancias'),('69','00AF-Frutas nat/legum/verduras'),('70','05AG-Funerarias,Velatorios'),('71','03KD-Galerias/expos/ferias/museos'),('72','01HA-Gobierno/camp gubernamental')
                    ,('73','00AS-Harinas/Tortillas/tostadas'),('74','00VE-Herramientas'),('75','01AM-Hielo'),('76','00SF-Higiene intima femenina'),('77','00OA-Hoteles'),('78','00ED-Iluminacion/pilas/focos/velas'),('79','03VA-Impermeabilizantes'),('80','00VD-Inmobiliarias'),('81','00LB-Insecticidas'),('82','00JA-Instrumentos/acc musicales')
                    ,('83','04SB-Jabon toc/shampoos piel'),('84','EA15-Jabon Lavatrastes'),('85','00JB-Juegos/juguetes'),('86','03BA-Jugos/nectares'),('87','SG15-Laxantes'),('88','00AG-Leches'),('89','00KC-Libros/revistas/Med impresos'),('90','00UA-Loterias/juegos de azar'),('91','01JE-Maletas/bolsas/portafolios'),('92','01AG-Mantequillas/margarinas')
                    ,('93','00MA-Maquinas/refacciones'),('94','04VA-Materiales p construcción'),('95','03SG-Medicamentos en General'),('96','00NB-Motocicletas'),('97','08SB-Pañales desechables'),('98','01LD-Palillos'),('99','00AA-Panificacion'),('100','02LD-Papel aluminio/encerado'),('101','06SB-Papel/pañuelo/servill desech'),
                     ('102','02HA-Partidos politicos'),('103','05KD-Peliculas/cines'),('104','05VA-Pisos/losetas/azulejos'),('105','02EB-Plateria general'),('106','03LD-Platos/vasos/cubiert desecha'),('107','00AP-Postres/mermelad/helados'),('108','00SD-Prod p higiene bucal'),('109','06SG-Productos contra el acné'),('110','07SB-Productos ortopédicos'),('111','05SG-Pruebas de embarazo'),('112','06VA-Puertas eléctricas/general')
                    ,('113','00PF-Pulpa de fruta'),('114','02AN-Pures'),('115','02AG-Quesos'),('116','01KB-Radio'),('117','00BA-Refrescos'),('118','00JF-Relojes/joyas'),('119','00OB-Restaurant/Gastron/Cnocturno'),('120','00RB-Ropa'),('121','03AN-Salsas'),('122','00FB-Seguros'),('123','05HB-Serv mensajería/paquetería'),('124','00FA-Serv. bancarios/financieros'),('125','02HB-Servicios de Salud'),('126','01SA-Shampoos/acondicionadores'),('127','03KB-Sist de televisión paga'),('128','00AD-Sopas'),('129','LC04-Suavizantes de ropa'),('130','03AG-Sustitutos de crema'),('131','00RA-Telas/hilos/acce p cost'),('132','00QA-Telecomunicaciones')
                    ,('133','00QB-Telefonia Celular'),('134','00CD-Telemercadeo'),('135','04CA-Tienda disco/cassette/video'),('136','01CA-Tiendas de autoservicio'),('137','03SA-Tintes p cabello'),('138','03SC-Toallas húmedas'),('139','08SG-Tratam p adelgazar'),('140','00OC-Turismo/viajes/Líneas aéreas'),('141','00OC-Turismo/viajes/Líneas aéreas'),('142','0001-Uso Interno Espacio Garantizad')
                    ,('143','00PT-Uso Interno Patrocinio'),('144','0003-Uso Interno Promoción'),('145','02KB-Uso Interno Promoción canal tv'),('146','00EB-Utensilios de cocina'),('147','08VA-Ventanas/vidrios/closets'),('148','09SB-Vigor sexual'),('149','09SG-Vitamina/complemen aliment'),('150','04AG-Yoghurts')], string='Categoría Televisa', track_visibility=True)


	target_primario = fields.Char(string='Target Primario', track_visibility=True)
	tarjet_secudario = fields.Char(string='Target Secundario', track_visibility=True)

	aaeetv_periodo_camp = fields.Char(string='Periodo de la Campaña', track_visibility=True)
	aaee_monto_maximo = fields.Float(string='Monto Máximo Propuesta (Costo Cliente)', track_visibility=True)
	aaee_monto_minimo = fields.Float(string='Monto Mínimo Propuesta (Costo Cliente)', track_visibility=True)
	aaeetv_2 = fields.Boolean(string='2', track_visibility=True)
	aaeetv_5 = fields.Boolean(string='5', track_visibility=True)
	aaeetv_9 = fields.Boolean(string='9', track_visibility=True)
	aaeetv_foro_tv = fields.Boolean(string='Foro TV', track_visibility=True)
	conoce_programas = fields.Char(string='Si conoce el(los) programa(s) indicar', track_visibility=True)

	box_bool = fields.Boolean(string='Box', track_visibility=True)
	canal5_bool = fields.Boolean(string='Canal 5', track_visibility=True)
	canal9_bool = fields.Boolean(string='Canal 9', track_visibility=True)
	comedia_bool = fields.Boolean(string='Comedia', track_visibility=True)
	revista_bool = fields.Boolean(string='De Revista', track_visibility=True)
	deportivos_bool = fields.Boolean(string='Deportivos', track_visibility=True)
	foro_tv_bool = fields.Boolean(string='Foro TV', track_visibility=True)
	lucha_bool = fields.Boolean(string='Lucha Libre', track_visibility=True)
	noticiero_bool = fields.Boolean(string='Noticieros', track_visibility=True)

	box_text = fields.Text(string='Acciones', track_visibility=True)
	canal5_text = fields.Text(string='Acciones', track_visibility=True)
	canal9_text = fields.Text(string='Acciones', track_visibility=True)
	comedia_text = fields.Text(string='Acciones', track_visibility=True)
	revista_text = fields.Text(string='Acciones', track_visibility=True)
	foro_tv_text = fields.Text(string='Acciones', track_visibility=True)
	lucha_text = fields.Text(string='Acciones', track_visibility=True)
	noticiero_text = fields.Text(string='Acciones', track_visibility=True)
	deportivo_text = fields.Text(string='Acciones', track_visibility=True)
	box_selection = fields.Selection([('1','Super'),('2','Banner'),('3','Mención 10"'),('4','Mención 20"'),('5','Cortinilla a corte'),('6','Patrocinio de Programa'),('7','Patrocinio de Sección')], string='Box', track_visibility=True)
	
	canal5_selection = fields.Selection([('1','Edición creativa'),('2','Cortinilla a corte'),('3','L en contenido'),('4','Patrocinio de programa'),('5','Promos Vea'),('6','Social TV'),('7','BUG (Logo)')], string='Canal 5', track_visibility=True)
	
	canal9_selection = fields.Selection([('1','Patrocinio de programa'),('2','Cortinilla a corte')],string='Canal 9', track_visibility=True)
	
	comedia_selection = fields.Selection([('1','Cortinilla a corte'),('2','Avance del Programa'),('3','Patrocinio de programa')],string='Comedia', track_visibility=True)
	
	revista_selection = fields.Selection([('1','Pleca'),('2','Super'),('3','Banner'),('4','Mención 30"'),('5','Mención 60"'),
								('6','Mención 120"'),('7','Promos Vea'),('8','Patrocinio de Programa'),('9','Patrocinio de sección'),
								('10','Entrevista 60"'),('11','Entrevista 120"'),('12','Bumper'),('13','Wiper')], string='De Revista', track_visibility=True)
	
	deportivos_selection = fields.Selection([('1','Pleca'),('2','Super'),('3','Banner'),('4','Cortinilla a corte'),
											 ('5','Promos Vea'),('6','Mención 30"'),('7','Mención 60"'),('8','Patrocinio de sección'),('9','Patrocinio de sección con pie'),('10','Patrocinio de programa')], string='Deportivos', track_visibility=True)
	
	foro_tv_selection = fields.Selection([('1','Entrevista'),('2','Desarrollo de Tema'),('3','Mención 60"'),('4','INT Activa con Mención de Marca'),
										  ('5','Integración Activa'),('6','Integración Ambiental"'),('7','Mención 60"'),('8','Patrocinio de sección (5" + 5")'),
										  ('9','Patrocinio de sección (5" + 5")+LOGO'),('10','Patrocinio programa')], string='Foro Tv', track_visibility=True)
	
	lucha_libre_selection = fields.Selection([('1','Super'),('2','Banner'),('3','Mención 10"'),('4','Mención 30"'),('5','Mención 60"'),('6','Mención 120"'),('7','Cortinilla a corte'),
									('8','Patrocinio de Programa'),('9','Patrocinio de Sección'),('10','Patrocinio de sección con pie')], string='Lucha Libre AAA', track_visibility=True)
	
	noticieros_selection = fields.Selection([('1','Pleca'),('2','Super'),('3','Banner'),('4','Cortinilla a corte'),('5','Promos Vea'),('6','Avance del Programa'),
								 ('7','Patrocinio de Programa'),('8','Patrocinio de sección'),('9','Resumen Informativo')],string='Noticieros', track_visibility=True)


	aaeetv_abierta_local_periodo_camp = fields.Char(string='Periodo de la campaña', track_visibility=True)
	tabla_plaza = fields.One2many('odt.medios.plaza','plazas_id')
	aaeetv_abierta_monto_maximo = fields.Float(string='Monto Máximo Propuesta (Costo cliente)', track_visibility=True)
	aaeetv_abierta_monto_maximo = fields.Float(string='Monto Mínimo Propuesta (Costo cliente)', track_visibility=True)
	aaeee_observations = fields.Text(string='Observaciones', track_visibility=True)

	# Brief aaee
	tv_abierta_bool = fields.Boolean(string='TV Abierta', track_visibility=True)
	tv_local_bool = fields.Boolean(string='TV Local', track_visibility=True)
	Network_bool = fields.Boolean(string='Network', track_visibility=True)
	area_comercial_selection = fields.Selection([('1','Gabriela Martínez'),('2','Maricarmen Lobo'),('3','Pamela Urrutia'),('4','Brenda Aguirre'),('5','Vanessa Fuentes'),('6','Alejandra Cárdenas')],string='Dirección Área Comercial', track_visibility=True)
	brief_presupuesto_minimo = fields.Float(string='Presupuesto Estimado mínimo (a costo cliente)', track_visibility=True)
	brief_presupuesto_maximo = fields.Float(string='Presupuesto Estimado máximo (a costo cliente)', track_visibility=True)
	braa_elabora = fields.Char(string='Elabora', track_visibility=True)
	braa_fecha = fields.Datetime(string='Fecha', track_visibility=True)
	braa_periodo = fields.Char(string='Periodo', track_visibility=True)
	braa_nombre_proyecto = fields.Char(string='Nombre o Tema del Proyecto', track_visibility=True)
	braa_descripcion_personalidad = fields.Text(string='Descripción y personalidad del producto', track_visibility=True)
	braa_objetivo = fields.Text(string='Objetivo', track_visibility=True)
	braa_idea_comunicar = fields.Text(string='Idea a Comunicar', track_visibility=True)
	braa_ambiente_contexto = fields.Text(string='Ambiente o contexto compatible', track_visibility=True)
	braa_talento_personaje = fields.Text(string='En caso de requerirse talento, Características de los personajes', track_visibility=True)
	braa_propuesta_idea = fields.Text(string='Propuesta o idea creativa (si la hay)', track_visibility=True)

	braa_opcion1 = fields.Boolean(string='Telenovela', track_visibility=True)
	braa_opcion2 = fields.Boolean(string='Revista', track_visibility=True)
	braa_opcion3 = fields.Boolean(string='Series', track_visibility=True)
	braa_opcion4 = fields.Boolean(string='Infantiles', track_visibility=True)
	braa_opcion5 = fields.Boolean(string='Repeticiones', track_visibility=True)
	braa_opcion6 = fields.Boolean(string='Reality', track_visibility=True)
	braa_opcion7 = fields.Boolean(string='Noticiero', track_visibility=True)
	braa_opcion8 = fields.Boolean(string='Comedia', track_visibility=True)
	braa_opcion9 = fields.Boolean(string='Deportivo', track_visibility=True)
	braa_opcion10 = fields.Boolean(string='Foro TV', track_visibility=True)

	braa_programa_especifico = fields.Text(string='Programa(s) Especifico(s) si ya se conoce(n)', track_visibility=True)
	braa_acciones = fields.Text(string='Acciones o Necesidades, Explicar: ', track_visibility=True)

	# Spoteo Carriers
	sc_marca_producto = fields.Char(string='Marca o Producto*')
	sc_catego_televisa = fields.Selection([('1','02SG-Algodon/Cotonetes'),('2','00AE-Alimentos en lata e instanta'),('3','00AI-Alimentos infantiles'),
                    ('4','00WB-Alimentos/art p animales'),('5','00CA-Almacen/mueble/Tdepartame'),('6','00JE-Anteojos/lentes de contacto '),
                    ('7','SG04-Antiacidos'),('8','04SG-Anticonceptivos/preservativos'),('9','SG09-Antigripal '),('10','00SH-Aparatos p la salud'),
                    ('11','00IA-Aparatos/acces de video'),('12','00IB-Aparatos/acces sonido'),('13','00LA-Art de limpieza en grl'),('14','00DA-Art deportivo/campamentos'),('15','00TA-Art/acces pcfumar /dejar de'),('16','00NA-Auromóviles/Automotores'),('17','00SG-Bandita/tela adhesiva/venda'),
                    ('18','01VA-Barnices/lacas/pinturas inter'),('19','01AO-Barras Alimenticias'),('20','00BB-Bebidas alcohólicas'),('21','02BA-Bebidas Isotónicas'),
                    ('22','00SC-Biberones/cosmet bebe'),('23','00RD-Blancos'),('24','00LD-Bolsas/plásticos desechables'),('25','00AC-Botanas'),('26','00AB-Cafes/tes/mod de leche'),('27','00RC-Calzado'),('28','00HA-Camp Cívicas/org no guber'),('29','02VA-Candados/cerrad protección'),('30','00AH-Carnes frías'),('31','00AM-Carnes/prod animales'),('32','03CA-Centros comerciales'),('33','02LA-Ceras'),
                    ('34','00AO-Cereales'),('35','01BB-Cerveza/bebid baja graduación'),('36','00AK-Chocolates/dulces/caramelos'),('37','03HB-Clinicas de belleza/estetica'),('38','01EC-Colchones'),('39','00NH-Combustib/lubricant auto'),('40','00PA-Computación'),('41','01KD-Congresos/simpos/conferenc'),('42','01AN-Consomes'),('43','00VB-Construcción y Vialidad'),('44','09SH-ConsumoResposable Alcohol'),('45','00SE-Cosmetico/maquill/desmaq'),('46','00SJ-Cremas/protectores p piel'),
                    ('47','01DB-Ctro de enteten/zoo/bal'),('48','04HB-Cupones/vales de despensa'),('49','00EE-Decoración/adornos hogar'),('50','002SE-Depiladores'),('51','02DB-Deportivos/gimnasios'),('52','02SB-Desodorantes/antitranspirantes')
                    ,('53','03LA-Destapacanos/desasolvadores'),('54','00LC-Detergentes/jabon p ropa'),('55','00IC-Discos/cassettes/compactos'),('56','01EB-Economizad/Purificad agua'),('57','00AJ-Edulcorante'),('58','00EA-Electrodomest/línea blanca'),('59','00XA-Equipo p oficina o escuela'),('60','00VC-Equipos industriales'),('61','00KA-Escuelas/Institutos/Cursos'),('62','02KD-Espectaculos/Teatro/Circo')
                    ,('63','03SB-Esponjas limpiad p piel'),('64','06CA-Farmacias'),('65','05CA-Ferreterias'),('66','00SA-Fijadores/tratam p cabello'),('67','00ID-Fotografia'),('68','00SI-Fragancias'),('69','00AF-Frutas nat/legum/verduras'),('70','05AG-Funerarias,Velatorios'),('71','03KD-Galerias/expos/ferias/museos'),('72','01HA-Gobierno/camp gubernamental')
                    ,('73','00AS-Harinas/Tortillas/tostadas'),('74','00VE-Herramientas'),('75','01AM-Hielo'),('76','00SF-Higiene intima femenina'),('77','00OA-Hoteles'),('78','00ED-Iluminacion/pilas/focos/velas'),('79','03VA-Impermeabilizantes'),('80','00VD-Inmobiliarias'),('81','00LB-Insecticidas'),('82','00JA-Instrumentos/acc musicales')
                    ,('83','04SB-Jabon toc/shampoos piel'),('84','EA15-Jabon Lavatrastes'),('85','00JB-Juegos/juguetes'),('86','03BA-Jugos/nectares'),('87','SG15-Laxantes'),('88','00AG-Leches'),('89','00KC-Libros/revistas/Med impresos'),('90','00UA-Loterias/juegos de azar'),('91','01JE-Maletas/bolsas/portafolios'),('92','01AG-Mantequillas/margarinas')
                    ,('93','00MA-Maquinas/refacciones'),('94','04VA-Materiales p construcción'),('95','03SG-Medicamentos en General'),('96','00NB-Motocicletas'),('97','08SB-Pañales desechables'),('98','01LD-Palillos'),('99','00AA-Panificacion'),('100','02LD-Papel aluminio/encerado'),('101','06SB-Papel/pañuelo/servill desech'),
                     ('102','02HA-Partidos politicos'),('103','05KD-Peliculas/cines'),('104','05VA-Pisos/losetas/azulejos'),('105','02EB-Plateria general'),('106','03LD-Platos/vasos/cubiert desecha'),('107','00AP-Postres/mermelad/helados'),('108','00SD-Prod p higiene bucal'),('109','06SG-Productos contra el acné'),('110','07SB-Productos ortopédicos'),('111','05SG-Pruebas de embarazo'),('112','06VA-Puertas eléctricas/general')
                    ,('113','00PF-Pulpa de fruta'),('114','02AN-Pures'),('115','02AG-Quesos'),('116','01KB-Radio'),('117','00BA-Refrescos'),('118','00JF-Relojes/joyas'),('119','00OB-Restaurant/Gastron/Cnocturno'),('120','00RB-Ropa'),('121','03AN-Salsas'),('122','00FB-Seguros'),('123','05HB-Serv mensajería/paquetería'),('124','00FA-Serv. bancarios/financieros'),('125','02HB-Servicios de Salud'),('126','01SA-Shampoos/acondicionadores'),('127','03KB-Sist de televisión paga'),('128','00AD-Sopas'),('129','LC04-Suavizantes de ropa'),('130','03AG-Sustitutos de crema'),('131','00RA-Telas/hilos/acce p cost'),('132','00QA-Telecomunicaciones')
                    ,('133','00QB-Telefonia Celular'),('134','00CD-Telemercadeo'),('135','04CA-Tienda disco/cassette/video'),('136','01CA-Tiendas de autoservicio'),('137','03SA-Tintes p cabello'),('138','03SC-Toallas húmedas'),('139','08SG-Tratam p adelgazar'),('140','00OC-Turismo/viajes/Líneas aéreas'),('141','00OC-Turismo/viajes/Líneas aéreas'),('142','0001-Uso Interno Espacio Garantizad')
                    ,('143','00PT-Uso Interno Patrocinio'),('144','0003-Uso Interno Promoción'),('145','02KB-Uso Interno Promoción canal tv'),('146','00EB-Utensilios de cocina'),('147','08VA-Ventanas/vidrios/closets'),('148','09SB-Vigor sexual'),('149','09SG-Vitamina/complemen aliment'),('150','04AG-Yoghurts')], string='Categoría Televisa', track_visibility=True)

	sc_target_primario = fields.Char(string='Target Primario', track_visibility=True)
	sc_target_secundario = fields.Char(string='Target Secundario', track_visibility=True)
	sc_monto_inversion = fields.Float(string='Monto Máximo inversión spoteo carriers (costo cliente)', track_visibility=True)
	sc_periodo_campana = fields.Char(string='Periodo de la Campaña', track_visibility=True)
	sc_duracion = fields.Selection([('1','10"'),('2','20"'),('3','30"'),('4','40"'),('5','50"'),('6','60"')], string='Duración de spot', track_visibility=True)
	sc_carriers = fields.Text(string='Carriers', track_visibility=True)
	sc_canales = fields.Selection([('1','Rank Rating'),('2','Afinidad Target')],string='Elección de Canales', track_visibility=True)
	sc_canales_conocen = fields.Text(string='Especifico si ya se conocen', track_visibility=True)
	sc_observaciones = fields.Text(string='Observaciones o restricciones', track_visibility=True)

	# network Televisa
	nt_marca = fields.Char(string='Marca o Producto*')
	nt_catego_televisa = fields.Selection([('1','02SG-Algodon/Cotonetes'),('2','00AE-Alimentos en lata e instanta'),('3','00AI-Alimentos infantiles'),
                    ('4','00WB-Alimentos/art p animales'),('5','00CA-Almacen/mueble/Tdepartame'),('6','00JE-Anteojos/lentes de contacto '),
                    ('7','SG04-Antiacidos'),('8','04SG-Anticonceptivos/preservativos'),('9','SG09-Antigripal '),('10','00SH-Aparatos p la salud'),
                    ('11','00IA-Aparatos/acces de video'),('12','00IB-Aparatos/acces sonido'),('13','00LA-Art de limpieza en grl'),('14','00DA-Art deportivo/campamentos'),('15','00TA-Art/acces pcfumar /dejar de'),('16','00NA-Auromóviles/Automotores'),('17','00SG-Bandita/tela adhesiva/venda'),
                    ('18','01VA-Barnices/lacas/pinturas inter'),('19','01AO-Barras Alimenticias'),('20','00BB-Bebidas alcohólicas'),('21','02BA-Bebidas Isotónicas'),
                    ('22','00SC-Biberones/cosmet bebe'),('23','00RD-Blancos'),('24','00LD-Bolsas/plasticos desechables'),('25','00AC-Botanas'),('26','00AB-Cafes/tes/mod de leche'),('27','00RC-Calzado'),('28','00HA-Camp Cívicas/org no guber'),('29','02VA-Candados/cerrad protección'),('30','00AH-Carnes frías'),('31','00AM-Carnes/prod animales'),('32','03CA-Centros comerciales'),('33','02LA-Ceras'),
                    ('34','00AO-Cereales'),('35','01BB-Cerveza/bebid baja graduación'),('36','00AK-Chocolates/dulces/caramelos'),('37','03HB-Clinicas de belleza/estetica'),('38','01EC-Colchones'),('39','00NH-Combustib/lubricant auto'),('40','00PA-Computación'),('41','01KD-Congresos/simpos/conferenc'),('42','01AN-Consomes'),('43','00VB-Construcción y Vialidad'),('44','09SH-ConsumoResposable Alcohol'),('45','00SE-Cosmetico/maquill/desmaq'),('46','00SJ-Cremas/protectores p piel'),
                    ('47','01DB-Ctro de enteten/zoo/bal'),('48','04HB-Cupones/vales de despensa'),('49','00EE-Decoración/adornos hogar'),('50','002SE-Depiladores'),('51','02DB-Deportivos/gimnasios'),('52','02SB-Desodorantes/antitranspirantes')
                    ,('53','03LA-Destapacanos/desasolvadores'),('54','00LC-Detergentes/jabon p ropa'),('55','00IC-Discos/cassettes/compactos'),('56','01EB-Economizad/Purificad agua'),('57','00AJ-Edulcorante'),('58','00EA-Electrodomest/línea blanca'),('59','00XA-Equipo p oficina o escuela'),('60','00VC-Equipos industriales'),('61','00KA-Escuelas/Institutos/Cursos'),('62','02KD-Espectaculos/Teatro/Circo')
                    ,('63','03SB-Esponjas limpiad p piel'),('64','06CA-Farmacias'),('65','05CA-Ferreterias'),('66','00SA-Fijadores/tratam p cabello'),('67','00ID-Fotografia'),('68','00SI-Fragancias'),('69','00AF-Frutas nat/legum/verduras'),('70','05AG-Funerarias,Velatorios'),('71','03KD-Galerias/expos/ferias/museos'),('72','01HA-Gobierno/camp gubernamental')
                    ,('73','00AS-Harinas/Tortillas/tostadas'),('74','00VE-Herramientas'),('75','01AM-Hielo'),('76','00SF-Higiene intima femenina'),('77','00OA-Hoteles'),('78','00ED-Iluminacion/pilas/focos/velas'),('79','03VA-Impermeabilizantes'),('80','00VD-Inmobiliarias'),('81','00LB-Insecticidas'),('82','00JA-Instrumentos/acc musicales')
                    ,('83','04SB-Jabon toc/shampoos piel'),('84','EA15-Jabon Lavatrastes'),('85','00JB-Juegos/juguetes'),('86','03BA-Jugos/nectares'),('87','SG15-Laxantes'),('88','00AG-Leches'),('89','00KC-Libros/revistas/Med impresos'),('90','00UA-Loterias/juegos de azar'),('91','01JE-Maletas/bolsas/portafolios'),('92','01AG-Mantequillas/margarinas')
                    ,('93','00MA-Maquinas/refacciones'),('94','04VA-Materiales p construcción'),('95','03SG-Medicamentos en General'),('96','00NB-Motocicletas'),('97','08SB-Pañales desechables'),('98','01LD-Palillos'),('99','00AA-Panificacion'),('100','02LD-Papel aluminio/encerado'),('101','06SB-Papel/pañuelo/servill desech'),
                     ('102','02HA-Partidos politicos'),('103','05KD-Peliculas/cines'),('104','05VA-Pisos/losetas/azulejos'),('105','02EB-Plateria general'),('106','03LD-Platos/vasos/cubiert desecha'),('107','00AP-Postres/mermelad/helados'),('108','00SD-Prod p higiene bucal'),('109','06SG-Productos contra el acné'),('110','07SB-Productos ortopédicos'),('111','05SG-Pruebas de embarazo'),('112','06VA-Puertas eléctricas/general')
                    ,('113','00PF-Pulpa de fruta'),('114','02AN-Pures'),('115','02AG-Quesos'),('116','01KB-Radio'),('117','00BA-Refrescos'),('118','00JF-Relojes/joyas'),('119','00OB-Restaurant/Gastron/Cnocturno'),('120','00RB-Ropa'),('121','03AN-Salsas'),('122','00FB-Seguros'),('123','05HB-Serv mensajería/paquetería'),('124','00FA-Serv. bancarios/financieros'),('125','02HB-Servicios de Salud'),('126','01SA-Shampoos/acondicionadores'),('127','03KB-Sist de televisión paga'),('128','00AD-Sopas'),('129','LC04-Suavizantes de ropa'),('130','03AG-Sustitutos de crema'),('131','00RA-Telas/hilos/acce p cost'),('132','00QA-Telecomunicaciones')
                    ,('133','00QB-Telefonia Celular'),('134','00CD-Telemercadeo'),('135','04CA-Tienda disco/cassette/video'),('136','01CA-Tiendas de autoservicio'),('137','03SA-Tintes p cabello'),('138','03SC-Toallas húmedas'),('139','08SG-Tratam p adelgazar'),('140','00OC-Turismo/viajes/Líneas aéreas'),('141','00OC-Turismo/viajes/Líneas aéreas'),('142','0001-Uso Interno Espacio Garantizad')
                    ,('143','00PT-Uso Interno Patrocinio'),('144','0003-Uso Interno Promoción'),('145','02KB-Uso Interno Promoción canal tv'),('146','00EB-Utensilios de cocina'),('147','08VA-Ventanas/vidrios/closets'),('148','09SB-Vigor sexual'),('149','09SG-Vitamina/complemen aliment'),('150','04AG-Yoghurts')], string='Categoría Televisa', track_visibility=True)

	nt_target_primario = fields.Char(string='Target Primario', track_visibility=True)
	nt_target_secundario = fields.Char(string='Target Secundario', track_visibility=True)
	nt_monto_inversion = fields.Float(string='Monto Máximo inversión spoteo carriers (costo cliente)', track_visibility=True)
	nt_periodo_campana = fields.Char(string='Periodo de la Campaña', track_visibility=True)
	nt_duracion = fields.Selection([('1','10"'),('2','20"'),('3','30"'),('4','40"'),('5','50"'),('6','60"')], string='Duración de spot*')
	nt_canales = fields.Many2many('canales.tags',string='Elección de Canales', track_visibility=True)
	nt_especifico = fields.Text(string='Específicos', track_visibility=True)
	nt_posicion = fields.Selection([('1','SI'),('2','NO')], string='Posicion', track_visibility=True)
	nt_observaciones = fields.Text(string='Observaciones o restricciones spoteo Networks Televisa: ', track_visibility=True)
	nt_aaee_inversion = fields.Float(string='Monto Máximo inversión AAEE Networks Televisa (costo cliente)', track_visibility=True)
	nt_aaee_periodo_campana = fields.Char(string='Periodo de la Campaña', track_visibility=True)
	nt_aaee_canales = fields.Selection([('1','Rank Rating'),('2','Afinidad Target')],string='Elección de Canales*')
	nt_aaee_especificos1 = fields.Selection([('1','Bandamax'),('2','De Película'),('3','De Película HD'),('4','De Película MPX'),('5','Distrito Comedia'),('6','Golden'),
											 ('7','Golden Edge'),('8','Golden HD'),('9','Golden MPX'),('10','Golden Premier'),('11','Ritmoson'),('12','TDN'),('13','TDN Univisión'),
											 ('14','Telehit'),('15','Telehit HD'),('16','TIIN'),('17','Tlenovelas'),('18','Unicable')], string='Específicos')
	nt_aaee_especificos2 = fields.Selection([('1','Bandamax'),('2','De Película'),('3','De Película HD'),('4','De Película MPX'),('5','Distrito Comedia'),('6','Golden'),
											 ('7','Golden Edge'),('8','Golden HD'),('9','Golden MPX'),('10','Golden Premier'),('11','Ritmoson'),('12','TDN'),('13','TDN Univisión'),
											 ('14','Telehit'),('15','Telehit HD'),('16','TIIN'),('17','Tlenovelas'),('18','Unicable')], string='Específicos', track_visibility=True)
	nt_aaee_programas = fields.Char(string='Si conoces el(los) programa(s) indicar')
	nt_aaee_deport = fields.Char(string='Deportivos')
	nt_aaee_revista = fields.Char(string='De Revista')
	nt_aaee_musicales = fields.Char(string='Musicales')
	nt_aaee_paquete_evento = fields.Text(string='Señalar si se requiere paquete para evento especifico (Ej.: NFL, Champions League...)')
	nt_aaee_observaciones = fields.Text(string='Observaciones o restricciones AAEE Networks Televisa: ')

	# Otros Networks
	ot_marca = fields.Char(string='Marca o Producto*')
	ot_target_primario = fields.Char(string='Target Primario')
	ot_target_secundario = fields.Char(string='Target Secundario')
	ot_monto_inversion = fields.Float(string='Monto Máximo inversión spoteo otros network*')
	ot_periodo_campana = fields.Char(string='Periodo de la Campaña*')
	ot_duracion = fields.Selection([('1','10"'),('2','20"'),('3','30"'),('4','40"'),('5','50"'),('6','60"')], string='Duración de spot*')
	ot_canales = fields.Selection([('1','Rank Rating'),('2','Afinidad Target')], string='Elección de Canales*')
	ot_especifico = fields.Text(string='Canales especificos')
	ot_posicion = fields.Selection([('1','SI'),('2','NO')], string='Posicion')
	ot_observaciones = fields.Text(string='Observaciones o restricciones spoteo otros Networks: ')
	
	ot_aaee_inversion = fields.Float(string='Monto Máximo inversión AAEE Networks (costo cliente)*')
	ot_aaee_periodo_campana = fields.Char(string='Periodo de la Campaña*')
	ot_aaee_especificos = fields.Char(string='Canales especificos')
	ot_aaee_canales = fields.Selection([('1','Rank Rating'),('2','Afinidad Target')],string='Elección de Canales*')
	ot_aaee_programa_especifico = fields.Text(string='Si conocen el(los) programa(s) indicar', track_visibility=True)
	ot_aaee_paquete_evento = fields.Text(string='Señalar si se requiere paquete para evento especifico (Ej.: NFL, Champions League...)')
	ot_aaee_observaciones = fields.Text(string='Observaciones o restricciones AAEE Networks: ')

	# Revista
	r_marca = fields.Char(string='Marca o Producto*')
	r_target_interes = fields.Char(string='Target de Interés*')
	r_periodo_campana = fields.Char(string='Periodo de la campaña*')
	r_monto_inversion = fields.Float(string='Inversión revistas(Costo Cliente)*')
	r_observaciones = fields.Text(string='Observaciones')
	tabla_medios_revista = fields.One2many('odt.medios.revista','revista_id')

	#Radio
	rad_marca = fields.Char(string='Marca o Producto*')
	rad_target_interes = fields.Char(string='Target de Interés*')
	rad_periodo_campana = fields.Char(string='Periodo de la campaña*')
	rad_monto_inversion = fields.Float(string='Inversión Radio (Costo Cliente)*')
	rad_observaciones = fields.Text(string='Observaciones')	
	tabla_medios_radio = fields.One2many('odt.medios.radio','radio_id')

	#ooh
	oh_marca = fields.Char(string='Marca o Producto')
	oh_target_interes = fields.Char(string='Target de Interés')
	oh_periodo_campana = fields.Char(string='Periodo de la campaña')
	oh_monto_inversion = fields.Float(string='Inversión OOH (Costo Cliente)')
	oh_tipo_actividad = fields.Selection([('1','Espectaculaes'),('2','Pantallas'),('3','Muros'),('4','Vallas'),('5','Parabuses'),('6','Puentes peatonales'),('7','Tren ligero'),('8','Metrobús'),
										  ('9','Metro'),('10','Mexibus'),('11','Mupis'),('12','Camiones Urbanos'),('13','Camiones escolares'),('14','Taxis'),('15','Aeropuerto'),('16','Pantallas en interiores'),
						 				  ('17','Plazas Comerciales'),('18','Bajo Puentes'),('19','Otros')],string='Tipo de Actividad')
	oh_observaciones = fields.Text(string='Comentarios')
	tabla_medios_ooh = fields.One2many('odt.medios.ooh','ooh_id')

	#Prensa
	p_marca = fields.Char(string='Marca o Producto*')
	p_target_interes = fields.Char(string='Target de Interés*')
	p_periodo_campana = fields.Char(string='Periodo de la campaña*')
	p_monto_inversion = fields.Float(string='Inversión Prensa (Costo Cliente)*')
	p_observaciones = fields.Text(string='Observaciones')		
	tabla_medios_prensa = fields.One2many('odt.medios.prensa','prensa_id')

	# Digital
	d_marca = fields.Char(string='Marca o Producto*')
	d_periodo_campana = fields.Char(string='Periodo de la campaña*')
	d_target_demo = fields.Char(string='Target Demográfico*')
	d_target_perfil = fields.Char(string='Target perfil Psicográfico*')
	d_objetivo_campana = fields.Text(string='Objetivo de la campaña*')
	d_option1 = fields.Boolean(string='Branding')
	d_option2 = fields.Boolean(string='Registros')
	d_option3 = fields.Boolean(string='Redes Sociales')
	d_option4 = fields.Boolean(string='Búsqueda')
	d_landing = fields.Char(string='Landing Page (Sólo si aplica)')
	d_description_campana = fields.Text(string='Descripción de la Campaña*')
	d_requerirlos = fields.Text(string='Enlistar los sitios específicos en caso de requerirlos:')
	d_folio_proyecto = fields.Char(string='Folio proyecto digital (si ya lo tiene)')
	d_monto_maximo = fields.Float(string='Monto Máximo Propuesta (Costos Cliente)*')
	d_monto_minimo = fields.Float(string='Monto Mínimo Propuesta (Costos Cliente)*')

	# Análisis
	an_inversion = fields.Boolean(string='Inversión Publicitaria')
	an_habitos = fields.Boolean(string='Hábitos')
	an_audiencia = fields.Boolean(string='Audiencias')
	an_otro = fields.Char(string='Otro: ')
	an_marca = fields.Char(string='Marca o Producto*')
	an_sector = fields.Char(string='Sector (NIELSEN/IBOPE)*')
	an_categoria = fields.Char(string='Categoria (NIELSEN/IBOPE)*')
	an_year_inmediato = fields.Boolean(string='Año Inmediato Anterior')
	an_year_movil = fields.Boolean(string='Año Móvil')
	an_periodo = fields.Char(string='Otro Periodo')
	an_analisis = fields.Text(string='Objetivo del Análisis. En caso de requerir comparativo de marcas especificas, señalarlo.')
	an_year_inmediato1 = fields.Boolean(string='Año Inmediato Anterior')
	an_year_movil1 = fields.Boolean(string='Año Móvil')
	an_periodo1 = fields.Char(string='Otro Periodo')
	an_target_interes = fields.Char(string='Target de interés*')
	an_analisis1 = fields.Text(string='Objetivo del Análisis.')	
	an_marca1 = fields.Char(string='Categoría o Marca/Producto de interés*')
	an_target_interes1 = fields.Char(string='Target de interés*')
	an_analisis2 = fields.Text(string='Objetivo del Análisis. (¿Qué se desea conocer?)')
	an_tro_descripcion = fields.Text(string='Describir el tipo de análisis y/o requerimientos de información.')

# class OdtMedios(models.Model):
# 	_name = 'odt.medios'
# 	_description = 'Ventana kanban para la estructura de medios'
# 	_inherit = ['mail.thread', 'mail.activity.mixin','crm.odt']


# 	presupuesto_cliente = fields.Float(string='Presupuesto del Cliente', track_visibility=True)
# 	# seccion para odt medios
# 	med_spot_tv_abierta = fields.Boolean(string='Spot TV Abierta TVSA', track_visibility=True)
# 	med_aaee_tv = fields.Boolean(string='AAEE TV TVSA', track_visibility=True)
# 	med_brief_aaee = fields.Boolean(string='Brief AAEE', track_visibility=True)
# 	med_spoteo_carriers = fields.Boolean(string='Spoteo Carriers', track_visibility=True)
# 	med_net_televisa = fields.Boolean(string='Networks Televisa', track_visibility=True)
# 	med_otros_net = fields.Boolean(string='Otros Networks', track_visibility=True)
# 	med_radio = fields.Boolean(string='Radio', track_visibility=True)
# 	med_revista = fields.Boolean(string='Revista', track_visibility=True)
# 	med_prensa = fields.Boolean(string='Prensa', track_visibility=True)
# 	med_ooh = fields.Boolean(string='OOH', track_visibility=True)
# 	med_digital = fields.Boolean(string='Digital', track_visibility=True)
# 	med_analisis = fields.Boolean(string='Analisis', track_visibility=True)

# 	#	Medios
# 	med_folio = fields.Char(string='Folio', track_visibility=True)
# 	med_fecha_soli = fields.Datetime(string='Fecha de solicitud', track_visibility=True)
# 	med_hora_soli = fields.Datetime(string='Hora de Solicitud', track_visibility=True)
# 	med_fecha_entrega = fields.Datetime(string='Fecha Estimada de Entrega', track_visibility=True)
# 	med_fecha_real = fields.Datetime(string='Fecha Real de Entrega', track_visibility=True)
# 	med_elabora = fields.Char(string='Elaborará este Plan', track_visibility=True)
# 	med_nivel_complejidad = fields.Char(string='Nivel de complejidad', track_visibility=True)

# 	# odt medios
# 	med_odt_fecha_entrega = fields.Datetime(string='Fecha de entrega solicitada', track_visibility=True)
# 	med_clave_proyecto = fields.Char(string='Clave de Proyecto', track_visibility=True)
# 	med_tipo_trabajo = fields.Selection([('1','Revisión de Pauta'),('2','Análisis'),('3','Plan de Medios')], string='Tipo de Trabajo Requerido', track_visibility=True)
# 	# Plan de medios
# 	med_objetivo_comunicacion = fields.Char(string='Objetivo de comunicación', track_visibility=True)
# 	med_presupuesto_cliente = fields.Char(string='Presupuesto Global Cliente', track_visibility=True)
# 	med_periodo_camap = fields.Char(string='Periodo camapaña y/o promoción', track_visibility=True)
# 	med_tipo_analisis = fields.Selection([('1','Inversión Publicitaria (Competencia)'),('2','Audiencia (Ratings)'),('3','Hábitos de Consumo (BIMSA)')],string='Tipo de Análisis', track_visibility=True)
# 	med_oberv_generales = fields.Text(string='Observaciones Generales', track_visibility=True)
# 	med_solicita = fields.Char(string='Nombre de quien solicita', track_visibility=True)
# 	med_getente = fields.Char(string='Gerente Medios', track_visibility=True)
# 	med_dirc_comercial = fields.Char(string='Dirección Comercial', track_visibility=True)
# 	med_icepresidencia = fields.Char(string='Vicepresidencia', track_visibility=True)

# 	#Solicitud TVSA
# 	tvsa_tipo_camp = fields.Selection([('1','TEASER'),('2','LANZAMIENTO'),('3','REGULAR')],string='Timpo de Campaña', track_visibility=True)
# 	tvsa_otro = fields.Char(string='Otro: (Especificar)')
# 	tvsa_catego_televisa = fields.Selection([('1','02SG-Algodon/Cotonetes'),('2','00AE-Alimentos en lata e instanta'),('3','00AI-Alimentos infantiles'),
#                     ('4','00WB-Alimentos/art p animales'),('5','00CA-Almacen/mueble/Tdepartame'),('6','00JE-Anteojos/lentes de contacto '),
#                     ('7','SG04-Antiacidos'),('8','04SG-Anticonceptivos/preservativos'),('9','SG09-Antigripal '),('10','00SH-Aparatos p la salud'),
#                     ('11','00IA-Aparatos/acces de video'),('12','00IB-Aparatos/acces sonido'),('13','00LA-Art de limpieza en grl'),('14','00DA-Art deportivo/campamentos'),('15','00TA-Art/acces pcfumar /dejar de'),('16','00NA-Auromóviles/Automotores'),('17','00SG-Bandita/tela adhesiva/venda'),
#                     ('18','01VA-Barnices/lacas/pinturas inter'),('19','01AO-Barras Alimenticias'),('20','00BB-Bebidas alcohólicas'),('21','02BA-Bebidas Isotonicas'),
#                     ('22','00SC-Biberones/cosmet bebe'),('23','00RD-Blancos'),('24','00LD-Bolsas/plasticos desechables'),('25','00AC-Botanas'),('26','00AB-Cafes/tes/mod de leche'),('27','00RC-Calzado'),('28','00HA-Camp Civicas/org no guber'),('29','02VA-Candados/cerrad protección'),('30','00AH-Carnes frias'),('31','00AM-Carnes/prod animales'),('32','03CA-Centros comerciales'),('33','02LA-Ceras'),
#                     ('34','00AO-Cereales'),('35','01BB-Cerveza/bedib baja graduación'),('36','00AK-Chocolates/dulces/caramelos'),('37','03HB-Clinicas de belleza/estetica'),('38','01EC-Colchones'),('39','00NH-Combustib/lubricant auto'),('40','00PA-Computación'),('41','01KD-Congresos/simpos/conferenc'),('42','01AN-Consomes'),('43','00VB-Construcción y Vialidad'),('44','09SH-ConsumoResposable Alcohol'),('45','00SE-Cosmetico/maquill/desmaq'),('46','00SJ-Cremas/protectores p piel'),
#                     ('47','01DB-Ctro de enteten/zoo/bal'),('48','04HB-Cupones/vales de despensa'),('49','00EE-Decoración/adornos hogar'),('50','002SE-Depiladores'),('51','02DB-Deportivos/gimnasios'),('52','02SB-Desodorantes/antitranspirantes')
#                     ,('53','03LA-Destapacanos/desasolvadores'),('54','00LC-Detergentes/jabon p ropa'),('55','00IC-Discos/cassettes/compactos'),('56','01EB-Economizad/Purificad agua'),('57','00AJ-Edulcorante'),('58','00EA-Electrodomest/linea blanca'),('59','00XA-Equipo p oficina o escuela'),('60','00VC-Equipos industriales'),('61','00KA-Escuelas/Institutos/Cursos'),('62','02KD-Espectaculos/Teatro/Circo')
#                     ,('63','03SB-Esponjas limpiad p piel'),('64','06CA-Farmacias'),('65','05CA-Ferreterias'),('66','00SA-Fijadores/tratam p cabello'),('67','00ID-Fotografia'),('68','00SI-Fragancias'),('69','00AF-Frutas nat/legum/verduras'),('70','05AG-Funerarias,Velatorios'),('71','03KD-Galerias/expos/ferias/museos'),('72','01HA-Gobierno/camp gubernamenta')
#                     ,('73','00AS-Harinas/Tortillas/tostadas'),('74','00VE-Herramientas'),('75','01AM-Hielo'),('76','00SF-Higiene intima femenina'),('77','00OA-Hoteles'),('78','00ED-Iluminacion/pilas/focos/velas'),('79','03VA-Impermeabilizantes'),('80','00VD-Inmobiliarias'),('81','00LB-Insecticidas'),('82','00JA-Instrumentos/acc musicales')
#                     ,('83','04SB-Jabon toc/shampoos piel'),('84','EA15-Jabon Lavatrastes'),('85','00JB-Juegos/juguetes'),('86','03BA-Jugos/nectares'),('87','SG15-Laxantes'),('88','00AG-Leches'),('89','00KC-Libros/revistas/Med impresos'),('90','00UA-Loterias/juegos de azar'),('91','01JE-Maletas/bolsas/portafolios'),('92','01AG-Mantequillas/margarinas')
#                     ,('93','00MA-Maquinas/refacciones'),('94','04VA-Materiales p construccion'),('95','03SG-Medicamentos en General'),('96','00NB-Motocicletas'),('97','08SB-Pañales desechables'),('98','01LD-Palillos'),('99','00AA-Panificacion'),('100','02LD-Papel aluminio/encerado'),('101','06SB-Papel/pañuelo/servill desech'),
#                      ('102','02HA-Partidos politicos'),('103','05KD-Peliculas/cines'),('104','05VA-Pisos/losetas/azulejos'),('105','02EB-Plateria general'),('106','03LD-Platos/vasos/cubiert desecha'),('107','00AP-Postres/mermelad/helados'),('108','00SD-Prod p higiene bucal'),('109','06SG-Productos contra el acne'),('110','07SB-Productos pedicos'),('111','05SG-Pruebas de embarazo'),('112','06VA-Puertas electricas/general')
#                     ,('113','00PF-Pulpa de fruta'),('114','02AN-Pures'),('115','02AG-Quesos'),('116','01KB-Radio'),('117','00BA-Refrescos'),('118','00JF-Relojes/joyas'),('119','00OB-Restaurant/Gastron/Cnocturno'),('120','00RB-Ropa'),('121','03AN-Salsas'),('122','00FB-Seguros'),('123','05HB-Serv mensajeria/paqueteria'),('124','00FA-Serv. bancarios/financieros'),('125','02HB-Servicios de Salud'),('126','01SA-Shampoos/acondicionadores'),('127','03KB-Sist de television paga'),('128','00AD-Sopas'),('129','LC04-Suavizantes de ropa'),('130','03AG-Sustitutos de crema'),('131','00RA-Telas/hilos/acce p cost'),('132','00QA-Telecomunicaciones')
#                     ,('133','00QB-Telefonia Celular'),('134','00CD-Telemercadeo'),('135','04CA-Tienda disco/cassette/video'),('136','01CA-Tiendas de autoservicio'),('137','03SA-Tintes p cabello'),('138','03SC-Toallas humedas'),('139','08SG-Tratam p adelgazar'),('140','00OC-Turismo/viajes/Lineas aereas'),('141','00OC-Turismo/viajes/Lineas aereas'),('142','0001-Uso Interno Espacio Garantizad')
#                     ,('143','00PT-Uso Interno Patrocinio'),('144','0003-Uso Interno Promocion'),('145','02KB-Uso Interno Promocion canal tv'),('146','00EB-Utensilios de cocina'),('147','08VA-Ventanas/vidrios/closets'),('148','09SB-Vigor sexual'),('149','09SG-Vitamina/complemen aliment'),('150','04AG-Yoghurts')], string='Categoria Televisa', track_visibility=True)

# 	tvsa_nse = fields.Selection([('1','ABC+ Alto + Medio alto'),('2','c Medio'),('3','D+ Medio Bajo'),('4','DE Bajo')], string="NSE", track_visibility=True)

# 	tvsa_grupo_edad_1 = fields.Boolean(string='4 - 12', track_visibility=True)
# 	tvsa_grupo_edad_2 = fields.Boolean(string='13 - 18', track_visibility=True)
# 	tvsa_grupo_edad_3 = fields.Boolean(string='19 - 29', track_visibility=True)
# 	tvsa_grupo_edad_4 = fields.Boolean(string='30 - 44', track_visibility=True)
# 	tvsa_grupo_edad_5 = fields.Boolean(string='45 - 54', track_visibility=True)
# 	tvsa_grupo_edad_6 = fields.Boolean(string='55+', track_visibility=True)
# 	tvsa_grupo_edad_otro = fields.Char(string='Otro', track_visibility=True)
# 	tvsa_sexo_p = fields.Boolean(string='Personas', track_visibility=True)
# 	tvsa_sexo_m = fields.Boolean(string='Mujeres', track_visibility=True)
# 	tvsa_sexo_h = fields.Boolean(string='Hombres', track_visibility=True)
# 	tvsa_rol_family = fields.Selection([('1','Jefes de Familia'),('2','Amas de Casa'),('3','Responsables de niños')],string='Rol Familiar', track_visibility=True)
# 	years_03 = fields.Boolean(string='0 a 3 años', track_visibility=True)
# 	years_48 = fields.Boolean(string='4 a 8 años', track_visibility=True)
# 	years_912 = fields.Boolean(string='9 a 12 años', track_visibility=True)
# 	target_secundario = fields.Char(string='Target Secundario', track_visibility=True)

# 	duracion_spot = fields.Char(string='Duración Spot', track_visibility=True)
# 	opcion_compra = fields.Selection([('1','CPR MODULOS'),('2','CPR FRANJAS'),('3','MIXTO MÓDULO Y FRANJA'),('4','CPR POR PROGRAMA'),('5','SPOTEO'),('6','SPOTEO COMPRA LIBRE')],string='Opciones de Compra', track_visibility=True)
# 	mixto_proporcion = fields.Char(string='En caso de ser Mixto especificar promoción', track_visibility=True)
# 	target_compra_modulo = fields.Char(string='Target de compra Módulos o Franja', track_visibility=True)
# 	target_especial = fields.Char(string='En caso de ser Target de compra Especial, Especificar', track_visibility=True)

# 	#regualcion
# 	cofepris = fields.Selection([('1','SI'),('2','NO')],string='COFEPRIS', track_visibility=True)
# 	a_favor = fields.Selection([('1','SI'),('2','NO')],string='A favor de lo mejor', track_visibility=True)
# 	kids_policy = fields.Selection([('1','SI'),('2','NO')],string='Kids Policy', track_visibility=True)
# 	sptv_periodo_camp1 = fields.Char(string='Periodo de la Campaña', track_visibility=True)
# 	canal_1 = fields.Boolean(string='2', track_visibility=True)
# 	canal_2 =  fields.Boolean(string='5', track_visibility=True)
# 	canal_3 =  fields.Boolean(string='9', track_visibility=True)
# 	tvsa_abierta = fields.Integer(string='Monto Máximo inversion TV abierta nacional (Costo clienten)', track_visibility=True)
# 	tv_abierta_duracion_spot = fields.Datetime(string='Duracion del Spot', track_visibility=True)

# 	canal_local = fields.Boolean(string='Canal Local', track_visibility=True)
# 	bloqueos = fields.Boolean(string='Bloqueos', track_visibility=True)
# 	sptv_periodo_camp2 = fields.Char(string='Periodo de la Campaña', track_visibility=True)
# 	foro_tv = fields.Boolean(string='Foro TV', track_visibility=True)
# 	foro_tv_descrip = fields.Text(string='Box', track_visibility=True)
# 	monto_inverison_tvabierta = fields.Float(string='Monto Maximo inversion TV Abierta Local (Costo Cliente)', track_visibility=True)
# 	tvsa_abierta_observaciones = fields.Text(string='Observaciones generales o condiciones especiales', track_visibility=True)

# 	# AAEETV
# 	aaee_categoria_televisa = fields.Selection([('1','02SG-Algodon/Cotonetes'),('2','00AE-Alimentos en lata e instanta'),('3','00AI-Alimentos infantiles'),
#                     ('4','00WB-Alimentos/art p animales'),('5','00CA-Almacen/mueble/Tdepartame'),('6','00JE-Anteojos/lentes de contacto '),
#                     ('7','SG04-Antiacidos'),('8','04SG-Anticonceptivos/preservativos'),('9','SG09-Antigripal '),('10','00SH-Aparatos p la salud'),
#                     ('11','00IA-Aparatos/acces de video'),('12','00IB-Aparatos/acces sonido'),('13','00LA-Art de limpieza en grl'),('14','00DA-Art deportivo/campamentos'),('15','00TA-Art/acces pcfumar /dejar de'),('16','00NA-Auromóviles/Automotores'),('17','00SG-Bandita/tela adhesiva/venda'),
#                     ('18','01VA-Barnices/lacas/pinturas inter'),('19','01AO-Barras Alimenticias'),('20','00BB-Bebidas alcohólicas'),('21','02BA-Bebidas Isotonicas'),
#                     ('22','00SC-Biberones/cosmet bebe'),('23','00RD-Blancos'),('24','00LD-Bolsas/plasticos desechables'),('25','00AC-Botanas'),('26','00AB-Cafes/tes/mod de leche'),('27','00RC-Calzado'),('28','00HA-Camp Civicas/org no guber'),('29','02VA-Candados/cerrad protección'),('30','00AH-Carnes frias'),('31','00AM-Carnes/prod animales'),('32','03CA-Centros comerciales'),('33','02LA-Ceras'),
#                     ('34','00AO-Cereales'),('35','01BB-Cerveza/bedib baja graduación'),('36','00AK-Chocolates/dulces/caramelos'),('37','03HB-Clinicas de belleza/estetica'),('38','01EC-Colchones'),('39','00NH-Combustib/lubricant auto'),('40','00PA-Computación'),('41','01KD-Congresos/simpos/conferenc'),('42','01AN-Consomes'),('43','00VB-Construcción y Vialidad'),('44','09SH-ConsumoResposable Alcohol'),('45','00SE-Cosmetico/maquill/desmaq'),('46','00SJ-Cremas/protectores p piel'),
#                     ('47','01DB-Ctro de enteten/zoo/bal'),('48','04HB-Cupones/vales de despensa'),('49','00EE-Decoración/adornos hogar'),('50','002SE-Depiladores'),('51','02DB-Deportivos/gimnasios'),('52','02SB-Desodorantes/antitranspirantes')
#                     ,('53','03LA-Destapacanos/desasolvadores'),('54','00LC-Detergentes/jabon p ropa'),('55','00IC-Discos/cassettes/compactos'),('56','01EB-Economizad/Purificad agua'),('57','00AJ-Edulcorante'),('58','00EA-Electrodomest/linea blanca'),('59','00XA-Equipo p oficina o escuela'),('60','00VC-Equipos industriales'),('61','00KA-Escuelas/Institutos/Cursos'),('62','02KD-Espectaculos/Teatro/Circo')
#                     ,('63','03SB-Esponjas limpiad p piel'),('64','06CA-Farmacias'),('65','05CA-Ferreterias'),('66','00SA-Fijadores/tratam p cabello'),('67','00ID-Fotografia'),('68','00SI-Fragancias'),('69','00AF-Frutas nat/legum/verduras'),('70','05AG-Funerarias,Velatorios'),('71','03KD-Galerias/expos/ferias/museos'),('72','01HA-Gobierno/camp gubernamenta')
#                     ,('73','00AS-Harinas/Tortillas/tostadas'),('74','00VE-Herramientas'),('75','01AM-Hielo'),('76','00SF-Higiene intima femenina'),('77','00OA-Hoteles'),('78','00ED-Iluminacion/pilas/focos/velas'),('79','03VA-Impermeabilizantes'),('80','00VD-Inmobiliarias'),('81','00LB-Insecticidas'),('82','00JA-Instrumentos/acc musicales')
#                     ,('83','04SB-Jabon toc/shampoos piel'),('84','EA15-Jabon Lavatrastes'),('85','00JB-Juegos/juguetes'),('86','03BA-Jugos/nectares'),('87','SG15-Laxantes'),('88','00AG-Leches'),('89','00KC-Libros/revistas/Med impresos'),('90','00UA-Loterias/juegos de azar'),('91','01JE-Maletas/bolsas/portafolios'),('92','01AG-Mantequillas/margarinas')
#                     ,('93','00MA-Maquinas/refacciones'),('94','04VA-Materiales p construccion'),('95','03SG-Medicamentos en General'),('96','00NB-Motocicletas'),('97','08SB-Pañales desechables'),('98','01LD-Palillos'),('99','00AA-Panificacion'),('100','02LD-Papel aluminio/encerado'),('101','06SB-Papel/pañuelo/servill desech'),
#                      ('102','02HA-Partidos politicos'),('103','05KD-Peliculas/cines'),('104','05VA-Pisos/losetas/azulejos'),('105','02EB-Plateria general'),('106','03LD-Platos/vasos/cubiert desecha'),('107','00AP-Postres/mermelad/helados'),('108','00SD-Prod p higiene bucal'),('109','06SG-Productos contra el acne'),('110','07SB-Productos pedicos'),('111','05SG-Pruebas de embarazo'),('112','06VA-Puertas electricas/general')
#                     ,('113','00PF-Pulpa de fruta'),('114','02AN-Pures'),('115','02AG-Quesos'),('116','01KB-Radio'),('117','00BA-Refrescos'),('118','00JF-Relojes/joyas'),('119','00OB-Restaurant/Gastron/Cnocturno'),('120','00RB-Ropa'),('121','03AN-Salsas'),('122','00FB-Seguros'),('123','05HB-Serv mensajeria/paqueteria'),('124','00FA-Serv. bancarios/financieros'),('125','02HB-Servicios de Salud'),('126','01SA-Shampoos/acondicionadores'),('127','03KB-Sist de television paga'),('128','00AD-Sopas'),('129','LC04-Suavizantes de ropa'),('130','03AG-Sustitutos de crema'),('131','00RA-Telas/hilos/acce p cost'),('132','00QA-Telecomunicaciones')
#                     ,('133','00QB-Telefonia Celular'),('134','00CD-Telemercadeo'),('135','04CA-Tienda disco/cassette/video'),('136','01CA-Tiendas de autoservicio'),('137','03SA-Tintes p cabello'),('138','03SC-Toallas humedas'),('139','08SG-Tratam p adelgazar'),('140','00OC-Turismo/viajes/Lineas aereas'),('141','00OC-Turismo/viajes/Lineas aereas'),('142','0001-Uso Interno Espacio Garantizad')
#                     ,('143','00PT-Uso Interno Patrocinio'),('144','0003-Uso Interno Promocion'),('145','02KB-Uso Interno Promocion canal tv'),('146','00EB-Utensilios de cocina'),('147','08VA-Ventanas/vidrios/closets'),('148','09SB-Vigor sexual'),('149','09SG-Vitamina/complemen aliment'),('150','04AG-Yoghurts')], string='Categoria Televisa', track_visibility=True)


# 	target_primario = fields.Char(string='Target Primario', track_visibility=True)
# 	tarjet_secudario = fields.Char(string='Target Secunndario', track_visibility=True)

# 	aaeetv_periodo_camp = fields.Char(string='Periodo de la Campaña', track_visibility=True)
# 	aaee_monto_maximo = fields.Float(string='Monto Máximon Propuesta (Costo Cliente)', track_visibility=True)
# 	aaee_monto_minimo = fields.Float(string='Monto Minimo Propuesta (Costo Cliente)', track_visibility=True)
# 	aaeetv_2 = fields.Boolean(string='2', track_visibility=True)
# 	aaeetv_5 = fields.Boolean(string='5', track_visibility=True)
# 	aaeetv_9 = fields.Boolean(string='9', track_visibility=True)
# 	aaeetv_foro_tv = fields.Boolean(string='Foro TV', track_visibility=True)
# 	conoce_programas = fields.Char(string='Si conoce el(los) programa(s) indicar', track_visibility=True)

# 	box_bool = fields.Boolean(string='Box', track_visibility=True)
# 	canal5_bool = fields.Boolean(string='Canal 5', track_visibility=True)
# 	canal9_bool = fields.Boolean(string='Canal 9', track_visibility=True)
# 	comedia_bool = fields.Boolean(string='Comedia', track_visibility=True)
# 	revista_bool = fields.Boolean(string='De Revista', track_visibility=True)
# 	deportivos_bool = fields.Boolean(string='Deportivos', track_visibility=True)
# 	foro_tv_bool = fields.Boolean(string='Foro TV', track_visibility=True)
# 	lucha_bool = fields.Boolean(string='Lucha Libre', track_visibility=True)
# 	noticiero_bool = fields.Boolean(string='Noticieros', track_visibility=True)

# 	box_text = fields.Text(string='Acciones', track_visibility=True)
# 	canal5_text = fields.Text(string='Acciones', track_visibility=True)
# 	canal9_text = fields.Text(string='Acciones', track_visibility=True)
# 	comedia_text = fields.Text(string='Acciones', track_visibility=True)
# 	revista_text = fields.Text(string='Acciones', track_visibility=True)
# 	foro_tv_text = fields.Text(string='Acciones', track_visibility=True)
# 	lucha_text = fields.Text(string='Acciones', track_visibility=True)
# 	noticiero_text = fields.Text(string='Acciones', track_visibility=True)
# 	deportivo_text = fields.Text(string='Acciones', track_visibility=True)
# 	box_selection = fields.Selection([('1','Super'),('2','Banner'),('3','Mención 10"'),('4','Mención 20"'),('5','Cortinilla a corte'),('6','Patrocinio de Programa'),('7','Patrocinio de Sección')], string='Box', track_visibility=True)
	
# 	canal5_selection = fields.Selection([('1','Edición creativa'),('2','Cortinilla a corte'),('3','L en contenido'),('4','Patrocinio de programa'),('5','Promos Vea'),('6','Social TV'),('7','BUG (Logo)')], string='Canal 5', track_visibility=True)
	
# 	canal9_selection = fields.Selection([('1','Patrocinio de programa'),('2','Cortinilla a corte')],string='Canal 9', track_visibility=True)
	
# 	comedia_selection = fields.Selection([('1','Cortinilla a corte'),('2','Avance del Programa'),('3','Patrocinio de programa')],string='Comedia', track_visibility=True)
	
# 	revista_selection = fields.Selection([('1','Pleca'),('2','Super'),('3','Banner'),('4','Mención 30"'),('5','Mención 60"'),
# 								('6','Mención 120"'),('7','Promos Vea'),('8','Patrocinio de Programa'),('9','Patrocinio de sección'),
# 								('10','Entrevista 60"'),('11','Entrevista 120"'),('12','Bumper'),('13','Wiper')], string='De Revista', track_visibility=True)
	
# 	deportivos_selection = fields.Selection([('1','Pleca'),('2','Super'),('3','Banner'),('4','Cortinilla a corte'),
# 											 ('5','Promos Vea'),('6','Mención 30"'),('7','Mención 60"'),('8','Patrocinio de sección'),('9','Patrocinio de sección con pie'),('10','Patrocinio de programa')], string='Deportivos', track_visibility=True)
	
# 	foro_tv_selection = fields.Selection([('1','Entrevista'),('2','Desarrollo de Tema'),('3','Mención 60"'),('4','INT Activa con Mención de Marca'),
# 										  ('5','Integración Activa'),('6','Integración Ambiental"'),('7','Mención 60"'),('8','Patrocinio de sección (5" + 5")'),
# 										  ('9','Patrocinio de sección (5" + 5")+LOGO'),('10','Patrocinio programa')], string='Foro Tv', track_visibility=True)
	
# 	lucha_libre_selection = fields.Selection([('1','Super'),('2','Banner'),('3','Mención 10"'),('4','Mención 30"'),('5','Mención 60"'),('6','Mención 120"'),('7','Cortinilla a corte'),
# 									('8','Patrocinio de Programa'),('9','Patrocinio de Sección'),('10','Patrocinio de sección con pie')], string='Lucha Libre AAA', track_visibility=True)
	
# 	noticieros_selection = fields.Selection([('1','Pleca'),('2','Super'),('3','Banner'),('4','Cortinilla a corte'),('5','Promos Vea'),('6','Avance del Programa'),
# 								 ('7','Patrocinio de Programa'),('8','Patrocinio de sección'),('9','Resumen Informativo')],string='Noticieros', track_visibility=True)


# 	aaeetv_abierta_local_periodo_camp = fields.Char(string='Periodo de la camapaña', track_visibility=True)
# 	tabla_plaza = fields.One2many('odt.medios.plaza','plazas_id')
# 	aaeetv_abierta_monto_maximo = fields.Float(string='Monto Maximo Propuesta (Costo cliente)', track_visibility=True)
# 	aaeetv_abierta_monto_maximo = fields.Float(string='Monto Minimo Propuesta (Costo cliente)', track_visibility=True)
# 	aaeee_observations = fields.Text(string='Observaciones', track_visibility=True)

# 	# Brief aaee
# 	tv_abierta_bool = fields.Boolean(string='TV Abierta', track_visibility=True)
# 	tv_local_bool = fields.Boolean(string='TV Local', track_visibility=True)
# 	Network_bool = fields.Boolean(string='Network', track_visibility=True)
# 	area_comercial_selection = fields.Selection([('1','Gabriela Martínez'),('2','Maricarmen Lobo'),('3','Pamela Urrutia'),('4','Brenda Aguirre'),('5','Vanessa Fuentes'),('6','Alejandra Cárdenas')],string='Dirección Área Comercial', track_visibility=True)
# 	brief_presupuesto_minimo = fields.Float(string='Presupuesto Estimado minimo (a costo cliente)', track_visibility=True)
# 	brief_presupuesto_maximo = fields.Float(string='Presupuesto Estimado maximo (a costo cliente)', track_visibility=True)
# 	braa_elabora = fields.Char(string='Elabora', track_visibility=True)
# 	braa_fecha = fields.Datetime(string='Fecha', track_visibility=True)
# 	braa_periodo = fields.Char(string='Periodo', track_visibility=True)
# 	braa_nombre_proyecto = fields.Char(string='Nombre o Tema del Proyecto', track_visibility=True)
# 	braa_descripcion_personalidad = fields.Text(string='Descrpición y personalidad del producto', track_visibility=True)
# 	braa_objetivo = fields.Text(string='Objetivo', track_visibility=True)
# 	braa_idea_comunicar = fields.Text(string='Idea a Comunicar', track_visibility=True)
# 	braa_ambiente_contexto = fields.Text(string='Ambiente o contexto compatible', track_visibility=True)
# 	braa_talento_personaje = fields.Text(string='En caso de requerirse talento, Caracteristicas de los personajes', track_visibility=True)
# 	braa_propuesta_idea = fields.Text(string='Propuesta o idea creativa (si la hay)', track_visibility=True)

# 	braa_opcion1 = fields.Boolean(string='Telenovela', track_visibility=True)
# 	braa_opcion2 = fields.Boolean(string='Revista', track_visibility=True)
# 	braa_opcion3 = fields.Boolean(string='Series', track_visibility=True)
# 	braa_opcion4 = fields.Boolean(string='Infantiles', track_visibility=True)
# 	braa_opcion5 = fields.Boolean(string='Repeticiones', track_visibility=True)
# 	braa_opcion6 = fields.Boolean(string='Reality', track_visibility=True)
# 	braa_opcion7 = fields.Boolean(string='Noticiero', track_visibility=True)
# 	braa_opcion8 = fields.Boolean(string='Comedia', track_visibility=True)
# 	braa_opcion9 = fields.Boolean(string='Deportivo', track_visibility=True)
# 	braa_opcion10 = fields.Boolean(string='Foro TV', track_visibility=True)

# 	braa_programa_especifico = fields.Text(string='Programa(s) Especifico(s) si ya se conoce(n)', track_visibility=True)
# 	braa_acciones = fields.Text(string='Acciones o Necesidades, Explicar: ', track_visibility=True)

# 	# Spoteo Carriers
# 	sc_marca_producto = fields.Char(string='Marca o Producto*')
# 	sc_catego_televisa = fields.Selection([('1','02SG-Algodon/Cotonetes'),('2','00AE-Alimentos en lata e instanta'),('3','00AI-Alimentos infantiles'),
#                     ('4','00WB-Alimentos/art p animales'),('5','00CA-Almacen/mueble/Tdepartame'),('6','00JE-Anteojos/lentes de contacto '),
#                     ('7','SG04-Antiacidos'),('8','04SG-Anticonceptivos/preservativos'),('9','SG09-Antigripal '),('10','00SH-Aparatos p la salud'),
#                     ('11','00IA-Aparatos/acces de video'),('12','00IB-Aparatos/acces sonido'),('13','00LA-Art de limpieza en grl'),('14','00DA-Art deportivo/campamentos'),('15','00TA-Art/acces pcfumar /dejar de'),('16','00NA-Auromóviles/Automotores'),('17','00SG-Bandita/tela adhesiva/venda'),
#                     ('18','01VA-Barnices/lacas/pinturas inter'),('19','01AO-Barras Alimenticias'),('20','00BB-Bebidas alcohólicas'),('21','02BA-Bebidas Isotonicas'),
#                     ('22','00SC-Biberones/cosmet bebe'),('23','00RD-Blancos'),('24','00LD-Bolsas/plasticos desechables'),('25','00AC-Botanas'),('26','00AB-Cafes/tes/mod de leche'),('27','00RC-Calzado'),('28','00HA-Camp Civicas/org no guber'),('29','02VA-Candados/cerrad protección'),('30','00AH-Carnes frias'),('31','00AM-Carnes/prod animales'),('32','03CA-Centros comerciales'),('33','02LA-Ceras'),
#                     ('34','00AO-Cereales'),('35','01BB-Cerveza/bedib baja graduación'),('36','00AK-Chocolates/dulces/caramelos'),('37','03HB-Clinicas de belleza/estetica'),('38','01EC-Colchones'),('39','00NH-Combustib/lubricant auto'),('40','00PA-Computación'),('41','01KD-Congresos/simpos/conferenc'),('42','01AN-Consomes'),('43','00VB-Construcción y Vialidad'),('44','09SH-ConsumoResposable Alcohol'),('45','00SE-Cosmetico/maquill/desmaq'),('46','00SJ-Cremas/protectores p piel'),
#                     ('47','01DB-Ctro de enteten/zoo/bal'),('48','04HB-Cupones/vales de despensa'),('49','00EE-Decoración/adornos hogar'),('50','002SE-Depiladores'),('51','02DB-Deportivos/gimnasios'),('52','02SB-Desodorantes/antitranspirantes')
#                     ,('53','03LA-Destapacanos/desasolvadores'),('54','00LC-Detergentes/jabon p ropa'),('55','00IC-Discos/cassettes/compactos'),('56','01EB-Economizad/Purificad agua'),('57','00AJ-Edulcorante'),('58','00EA-Electrodomest/linea blanca'),('59','00XA-Equipo p oficina o escuela'),('60','00VC-Equipos industriales'),('61','00KA-Escuelas/Institutos/Cursos'),('62','02KD-Espectaculos/Teatro/Circo')
#                     ,('63','03SB-Esponjas limpiad p piel'),('64','06CA-Farmacias'),('65','05CA-Ferreterias'),('66','00SA-Fijadores/tratam p cabello'),('67','00ID-Fotografia'),('68','00SI-Fragancias'),('69','00AF-Frutas nat/legum/verduras'),('70','05AG-Funerarias,Velatorios'),('71','03KD-Galerias/expos/ferias/museos'),('72','01HA-Gobierno/camp gubernamenta')
#                     ,('73','00AS-Harinas/Tortillas/tostadas'),('74','00VE-Herramientas'),('75','01AM-Hielo'),('76','00SF-Higiene intima femenina'),('77','00OA-Hoteles'),('78','00ED-Iluminacion/pilas/focos/velas'),('79','03VA-Impermeabilizantes'),('80','00VD-Inmobiliarias'),('81','00LB-Insecticidas'),('82','00JA-Instrumentos/acc musicales')
#                     ,('83','04SB-Jabon toc/shampoos piel'),('84','EA15-Jabon Lavatrastes'),('85','00JB-Juegos/juguetes'),('86','03BA-Jugos/nectares'),('87','SG15-Laxantes'),('88','00AG-Leches'),('89','00KC-Libros/revistas/Med impresos'),('90','00UA-Loterias/juegos de azar'),('91','01JE-Maletas/bolsas/portafolios'),('92','01AG-Mantequillas/margarinas')
#                     ,('93','00MA-Maquinas/refacciones'),('94','04VA-Materiales p construccion'),('95','03SG-Medicamentos en General'),('96','00NB-Motocicletas'),('97','08SB-Pañales desechables'),('98','01LD-Palillos'),('99','00AA-Panificacion'),('100','02LD-Papel aluminio/encerado'),('101','06SB-Papel/pañuelo/servill desech'),
#                      ('102','02HA-Partidos politicos'),('103','05KD-Peliculas/cines'),('104','05VA-Pisos/losetas/azulejos'),('105','02EB-Plateria general'),('106','03LD-Platos/vasos/cubiert desecha'),('107','00AP-Postres/mermelad/helados'),('108','00SD-Prod p higiene bucal'),('109','06SG-Productos contra el acne'),('110','07SB-Productos pedicos'),('111','05SG-Pruebas de embarazo'),('112','06VA-Puertas electricas/general')
#                     ,('113','00PF-Pulpa de fruta'),('114','02AN-Pures'),('115','02AG-Quesos'),('116','01KB-Radio'),('117','00BA-Refrescos'),('118','00JF-Relojes/joyas'),('119','00OB-Restaurant/Gastron/Cnocturno'),('120','00RB-Ropa'),('121','03AN-Salsas'),('122','00FB-Seguros'),('123','05HB-Serv mensajeria/paqueteria'),('124','00FA-Serv. bancarios/financieros'),('125','02HB-Servicios de Salud'),('126','01SA-Shampoos/acondicionadores'),('127','03KB-Sist de television paga'),('128','00AD-Sopas'),('129','LC04-Suavizantes de ropa'),('130','03AG-Sustitutos de crema'),('131','00RA-Telas/hilos/acce p cost'),('132','00QA-Telecomunicaciones')
#                     ,('133','00QB-Telefonia Celular'),('134','00CD-Telemercadeo'),('135','04CA-Tienda disco/cassette/video'),('136','01CA-Tiendas de autoservicio'),('137','03SA-Tintes p cabello'),('138','03SC-Toallas humedas'),('139','08SG-Tratam p adelgazar'),('140','00OC-Turismo/viajes/Lineas aereas'),('141','00OC-Turismo/viajes/Lineas aereas'),('142','0001-Uso Interno Espacio Garantizad')
#                     ,('143','00PT-Uso Interno Patrocinio'),('144','0003-Uso Interno Promocion'),('145','02KB-Uso Interno Promocion canal tv'),('146','00EB-Utensilios de cocina'),('147','08VA-Ventanas/vidrios/closets'),('148','09SB-Vigor sexual'),('149','09SG-Vitamina/complemen aliment'),('150','04AG-Yoghurts')], string='Categoria Televisa', track_visibility=True)

# 	sc_target_primario = fields.Char(string='Target Primario')
# 	sc_target_secundario = fields.Char(string='Target Secundario')
# 	sc_monto_inversion = fields.Float(string='Monto Máximo inversión spoteo carriers (costo cliente)*')
# 	sc_periodo_campana = fields.Char(string='Preiodo de la Campaña*')
# 	sc_duracion = fields.Selection([('1','10"'),('2','20"'),('3','30"'),('4','40"'),('5','50"'),('6','60"')], string='Duración de spot*')
# 	sc_carriers = fields.Text(string='Carriers')
# 	sc_canales = fields.Selection([('1','Rank Rating'),('2','Afinidad Target')],string='Elección de Canales*')
# 	sc_canales_conocen = fields.Text(string='Especifico si ya se conocen')
# 	sc_observaciones = fields.Text(string='Observaciones o restricciones')

# 	# network Televisa
# 	nt_marca = fields.Char(string='Marca o Producto*')
# 	nt_catego_televisa = fields.Selection([('1','02SG-Algodon/Cotonetes'),('2','00AE-Alimentos en lata e instanta'),('3','00AI-Alimentos infantiles'),
#                     ('4','00WB-Alimentos/art p animales'),('5','00CA-Almacen/mueble/Tdepartame'),('6','00JE-Anteojos/lentes de contacto '),
#                     ('7','SG04-Antiacidos'),('8','04SG-Anticonceptivos/preservativos'),('9','SG09-Antigripal '),('10','00SH-Aparatos p la salud'),
#                     ('11','00IA-Aparatos/acces de video'),('12','00IB-Aparatos/acces sonido'),('13','00LA-Art de limpieza en grl'),('14','00DA-Art deportivo/campamentos'),('15','00TA-Art/acces pcfumar /dejar de'),('16','00NA-Auromóviles/Automotores'),('17','00SG-Bandita/tela adhesiva/venda'),
#                     ('18','01VA-Barnices/lacas/pinturas inter'),('19','01AO-Barras Alimenticias'),('20','00BB-Bebidas alcohólicas'),('21','02BA-Bebidas Isotonicas'),
#                     ('22','00SC-Biberones/cosmet bebe'),('23','00RD-Blancos'),('24','00LD-Bolsas/plasticos desechables'),('25','00AC-Botanas'),('26','00AB-Cafes/tes/mod de leche'),('27','00RC-Calzado'),('28','00HA-Camp Civicas/org no guber'),('29','02VA-Candados/cerrad protección'),('30','00AH-Carnes frias'),('31','00AM-Carnes/prod animales'),('32','03CA-Centros comerciales'),('33','02LA-Ceras'),
#                     ('34','00AO-Cereales'),('35','01BB-Cerveza/bedib baja graduación'),('36','00AK-Chocolates/dulces/caramelos'),('37','03HB-Clinicas de belleza/estetica'),('38','01EC-Colchones'),('39','00NH-Combustib/lubricant auto'),('40','00PA-Computación'),('41','01KD-Congresos/simpos/conferenc'),('42','01AN-Consomes'),('43','00VB-Construcción y Vialidad'),('44','09SH-ConsumoResposable Alcohol'),('45','00SE-Cosmetico/maquill/desmaq'),('46','00SJ-Cremas/protectores p piel'),
#                     ('47','01DB-Ctro de enteten/zoo/bal'),('48','04HB-Cupones/vales de despensa'),('49','00EE-Decoración/adornos hogar'),('50','002SE-Depiladores'),('51','02DB-Deportivos/gimnasios'),('52','02SB-Desodorantes/antitranspirantes')
#                     ,('53','03LA-Destapacanos/desasolvadores'),('54','00LC-Detergentes/jabon p ropa'),('55','00IC-Discos/cassettes/compactos'),('56','01EB-Economizad/Purificad agua'),('57','00AJ-Edulcorante'),('58','00EA-Electrodomest/linea blanca'),('59','00XA-Equipo p oficina o escuela'),('60','00VC-Equipos industriales'),('61','00KA-Escuelas/Institutos/Cursos'),('62','02KD-Espectaculos/Teatro/Circo')
#                     ,('63','03SB-Esponjas limpiad p piel'),('64','06CA-Farmacias'),('65','05CA-Ferreterias'),('66','00SA-Fijadores/tratam p cabello'),('67','00ID-Fotografia'),('68','00SI-Fragancias'),('69','00AF-Frutas nat/legum/verduras'),('70','05AG-Funerarias,Velatorios'),('71','03KD-Galerias/expos/ferias/museos'),('72','01HA-Gobierno/camp gubernamenta')
#                     ,('73','00AS-Harinas/Tortillas/tostadas'),('74','00VE-Herramientas'),('75','01AM-Hielo'),('76','00SF-Higiene intima femenina'),('77','00OA-Hoteles'),('78','00ED-Iluminacion/pilas/focos/velas'),('79','03VA-Impermeabilizantes'),('80','00VD-Inmobiliarias'),('81','00LB-Insecticidas'),('82','00JA-Instrumentos/acc musicales')
#                     ,('83','04SB-Jabon toc/shampoos piel'),('84','EA15-Jabon Lavatrastes'),('85','00JB-Juegos/juguetes'),('86','03BA-Jugos/nectares'),('87','SG15-Laxantes'),('88','00AG-Leches'),('89','00KC-Libros/revistas/Med impresos'),('90','00UA-Loterias/juegos de azar'),('91','01JE-Maletas/bolsas/portafolios'),('92','01AG-Mantequillas/margarinas')
#                     ,('93','00MA-Maquinas/refacciones'),('94','04VA-Materiales p construccion'),('95','03SG-Medicamentos en General'),('96','00NB-Motocicletas'),('97','08SB-Pañales desechables'),('98','01LD-Palillos'),('99','00AA-Panificacion'),('100','02LD-Papel aluminio/encerado'),('101','06SB-Papel/pañuelo/servill desech'),
#                      ('102','02HA-Partidos politicos'),('103','05KD-Peliculas/cines'),('104','05VA-Pisos/losetas/azulejos'),('105','02EB-Plateria general'),('106','03LD-Platos/vasos/cubiert desecha'),('107','00AP-Postres/mermelad/helados'),('108','00SD-Prod p higiene bucal'),('109','06SG-Productos contra el acne'),('110','07SB-Productos pedicos'),('111','05SG-Pruebas de embarazo'),('112','06VA-Puertas electricas/general')
#                     ,('113','00PF-Pulpa de fruta'),('114','02AN-Pures'),('115','02AG-Quesos'),('116','01KB-Radio'),('117','00BA-Refrescos'),('118','00JF-Relojes/joyas'),('119','00OB-Restaurant/Gastron/Cnocturno'),('120','00RB-Ropa'),('121','03AN-Salsas'),('122','00FB-Seguros'),('123','05HB-Serv mensajeria/paqueteria'),('124','00FA-Serv. bancarios/financieros'),('125','02HB-Servicios de Salud'),('126','01SA-Shampoos/acondicionadores'),('127','03KB-Sist de television paga'),('128','00AD-Sopas'),('129','LC04-Suavizantes de ropa'),('130','03AG-Sustitutos de crema'),('131','00RA-Telas/hilos/acce p cost'),('132','00QA-Telecomunicaciones')
#                     ,('133','00QB-Telefonia Celular'),('134','00CD-Telemercadeo'),('135','04CA-Tienda disco/cassette/video'),('136','01CA-Tiendas de autoservicio'),('137','03SA-Tintes p cabello'),('138','03SC-Toallas humedas'),('139','08SG-Tratam p adelgazar'),('140','00OC-Turismo/viajes/Lineas aereas'),('141','00OC-Turismo/viajes/Lineas aereas'),('142','0001-Uso Interno Espacio Garantizad')
#                     ,('143','00PT-Uso Interno Patrocinio'),('144','0003-Uso Interno Promocion'),('145','02KB-Uso Interno Promocion canal tv'),('146','00EB-Utensilios de cocina'),('147','08VA-Ventanas/vidrios/closets'),('148','09SB-Vigor sexual'),('149','09SG-Vitamina/complemen aliment'),('150','04AG-Yoghurts')], string='Categoria Televisa', track_visibility=True)

# 	nt_target_primario = fields.Char(string='Target Primario')
# 	nt_target_secundario = fields.Char(string='Target Secundario')
# 	nt_monto_inversion = fields.Float(string='Monto Máximo inversión spoteo carriers (costo cliente)*')
# 	nt_periodo_campana = fields.Char(string='Preiodo de la Campaña*')
# 	nt_duracion = fields.Selection([('1','10"'),('2','20"'),('3','30"'),('4','40"'),('5','50"'),('6','60"')], string='Duración de spot*')
# 	nt_canales = fields.Selection([('1','Rank Rating'),('2','Afinidad Target')], string='Elección de Canales*')
# 	nt_especifico = fields.Text(string='Especificos')
# 	nt_posicion = fields.Selection([('1','SI'),('2','NO')], string=' ')
# 	nt_observaciones = fields.Text(string='Observaciones o restricciones spoteo Networks Televisa: ')
# 	nt_aaee_inversion = fields.Float(string='Monto Maximo inversión AAEE Networks Televisa (costo cliente)*')
# 	nt_aaee_periodo_campana = fields.Char(string='Periodo de la Campaña*')
# 	nt_aaee_canales = fields.Selection([('1','Rank Rating'),('2','Afinidad Target')],string='Elección de Canales*')
# 	nt_aaee_especificos1 = fields.Selection([('1','Bandamax'),('2','De Pelicula'),('3','De Pelicula HD'),('4','De Pelicula MPX'),('5','Distrito Comedia'),('6','Golden'),
# 											 ('7','Golden Edge'),('8','Golden HD'),('9','Golden MPX'),('10','Golden Premier'),('11','Ritmoson'),('12','TDN'),('13','TDN Univisión'),
# 											 ('14','Telehit'),('15','Telehit HD'),('16','TIIN'),('17','Tlenovelas'),('18','Unicable')], string='Especificos')
# 	nt_aaee_especificos2 = fields.Selection([('1','Bandamax'),('2','De Pelicula'),('3','De Pelicula HD'),('4','De Pelicula MPX'),('5','Distrito Comedia'),('6','Golden'),
# 											 ('7','Golden Edge'),('8','Golden HD'),('9','Golden MPX'),('10','Golden Premier'),('11','Ritmoson'),('12','TDN'),('13','TDN Univisión'),
# 											 ('14','Telehit'),('15','Telehit HD'),('16','TIIN'),('17','Tlenovelas'),('18','Unicable')], string='Especificos')
# 	nt_aaee_programas = fields.Char(string='Si conoces el(los) programa(s) indicar')
# 	nt_aaee_deport = fields.Char(string='Deportivos')
# 	nt_aaee_revista = fields.Char(string='De Revista')
# 	nt_aaee_musicales = fields.Char(string='Musicales')
# 	nt_aaee_paquete_evento = fields.Text(string='Señalar si se requiere paquete para evento especifico (Ej.: NFL, Champions League...)')
# 	nt_aaee_observaciones = fields.Text(string='Observaciones o restricciones AAEE Networks Televisa: ')

# 	# Otros Networks
# 	ot_marca = fields.Char(string='Marca o Producto*')
# 	ot_target_primario = fields.Char(string='Target Primario')
# 	ot_target_secundario = fields.Char(string='Target Secundario')
# 	ot_monto_inversion = fields.Float(string='Monto Máximo inversión spoteo otros network*')
# 	ot_periodo_campana = fields.Char(string='Preiodo de la Campaña*')
# 	ot_duracion = fields.Selection([('1','10"'),('2','20"'),('3','30"'),('4','40"'),('5','50"'),('6','60"')], string='Duración de spot*')
# 	ot_canales = fields.Selection([('1','Rank Rating'),('2','Afinidad Target')], string='Elección de Canales*')
# 	ot_especifico = fields.Text(string='Especificos')
# 	ot_posicion = fields.Selection([('1','SI'),('2','NO')], string=' ')
# 	ot_observaciones = fields.Text(string='Observaciones o restricciones spoteo otros Networks: ')
	
# 	ot_aaee_inversion = fields.Float(string='Monto Maximo inversión AAEE Networks (costo cliente)*')
# 	ot_aaee_periodo_campana = fields.Char(string='Periodo de la Campaña*')
# 	ot_aaee_especificos = fields.Char(string='Especificos')
# 	ot_aaee_canales = fields.Selection([('1','Rank Rating'),('2','Afinidad Target')],string='Elección de Canales*')
# 	ot_aaee_programa_especifico = fields.Text(string='Si conocen el(los) programa(s) indicar', track_visibility=True)
# 	ot_aaee_paquete_evento = fields.Text(string='Señalar si se requiere paquete para evento especifico (Ej.: NFL, Champions League...)')
# 	ot_aaee_observaciones = fields.Text(string='Observaciones o restricciones AAEE Networks: ')

# 	# Revista
# 	r_marca = fields.Char(string='Marca o Producto*')
# 	r_target_interes = fields.Char(string='Target de Interés*')
# 	r_periodo_campana = fields.Char(string='Periodo de la camapaña*')
# 	r_monto_inversion = fields.Float(string='Inversión revistas(Costo Cliente)*')
# 	r_tamano_insercion = fields.Selection([('1','Página'),('2','Página impar'),('3','Spread'),('4','Cuarta de forros'),('5','Tercera de forros'),('6','Otro')],string='Tamaño de Inserción Regular')
# 	r_tipo_creatividad = fields.Selection([('1','Publireportaje'),('2','Gatefold'),('3','Encarte'),('4','Suajes'),('5','Fajilla'),('6','Otro')],string='Tipo (Creatividades)')
# 	r_observaciones = fields.Text(string='Observaciones')
# 	tabla_medios_revista = fields.One2many('odt.medios.revista','revista_id')

# 	#Radio
# 	rad_marca = fields.Char(string='Marca o Producto*')
# 	rad_target_interes = fields.Char(string='Target de Interés*')
# 	rad_periodo_campana = fields.Char(string='Periodo de la camapaña*')
# 	rad_monto_inversion = fields.Float(string='Inversión Radio (Costo Cliente)*')
# 	rad_tipo = fields.Selection([('1','Spoteo'),('2','Manción 1'),('3','Cápsula 1'),('4','Patrocinio'),('5','Enlaces'),('6','Entrevista'),('7','Otro')],string='Tipo*')
# 	rad_observaciones = fields.Text(string='Observaciones')	
# 	tabla_medios_radio = fields.One2many('odt.medios.radio','radio_id')

# 	#ooh
# 	oh_marca = fields.Char(string='Marca o Producto*')
# 	oh_target_interes = fields.Char(string='Target de Interés*')
# 	oh_periodo_campana = fields.Char(string='Periodo de la camapaña*')
# 	oh_monto_inversion = fields.Float(string='Inversión OOH (Costo Cliente)*')
# 	oh_tipo_actividad = fields.Selection([('1','Espectaculaes'),('2','Pantallas'),('3','Muros'),('4','Vallas'),('5','Parabuses'),('6','Puentes peatonales'),('7','Tren ligero'),('8','Metrobús'),
# 										  ('9','Metro'),('10','Mexibus'),('11','Mupis'),('12','Camiones Urbanos'),('13','Camiones escolares'),('14','Taxis'),('15','Aeropuerto'),('16','Pantallas en interiores'),
# 						 				  ('17','Plazas Comerciales'),('18','Bajo Puentes'),('19','Otros')],string='Tipo de Activadad')
# 	oh_observaciones = fields.Text(string='Comentarios')
# 	tabla_medios_ooh = fields.One2many('odt.medios.ooh','ooh_id')

# 	#Prensa
# 	p_marca = fields.Char(string='Marca o Producto*')
# 	p_target_interes = fields.Char(string='Target de Interés*')
# 	p_periodo_campana = fields.Char(string='Periodo de la camapaña*')
# 	p_monto_inversion = fields.Float(string='Inversión Prensa (Costo Cliente)*')
# 	p_tamano = fields.Selection([('1','Plana'),('2','Robaplana'),('3','1/2 Plana Horizontal'),('4','1/2 Plana Vertical'),('5','1/4 Plana'),('6','1/8 Plana'),('7','Otro')],string='Tamaño*')
# 	p_observaciones = fields.Text(string='Observaciones')		
# 	tabla_medios_prensa = fields.One2many('odt.medios.prensa','prensa_id')

# 	# Digital
# 	d_marca = fields.Char(string='Marca o Producto*')
# 	d_periodo_campana = fields.Char(string='Periodo de la camapaña*')
# 	d_target_demo = fields.Char(string='Target Demográfico*')
# 	d_target_perfil = fields.Char(string='Target perfil Psicográfico*')
# 	d_objetivo_campana = fields.Text(string='Objetivo de la camapaña*')
# 	d_option1 = fields.Boolean(string='Branding')
# 	d_option2 = fields.Boolean(string='Registros')
# 	d_option3 = fields.Boolean(string='Redes Sociales')
# 	d_option4 = fields.Boolean(string='Búsqueda')
# 	d_landing = fields.Char(string='Landing Page (Sólo si aplica)')
# 	d_description_campana = fields.Text(string='Descrpición de la Campaña*')
# 	d_requerirlos = fields.Text(string='Enlistar los sitios especificos en caso de requerirlos:')
# 	d_folio_proyecto = fields.Char(string='Folio proyecto digital (si ya lo tiene)')
# 	d_monto_maximo = fields.Float(string='Monto Máximo Propuesta (Costos Cliente)*')
# 	d_monto_minimo = fields.Float(string='Monto Minimo Propuesta (Costos Cliente)*')

# 	# Analisis
# 	an_inversion = fields.Boolean(string='Inversión Publicitaria')
# 	an_habitos = fields.Boolean(string='Hábitos')
# 	an_audiencia = fields.Boolean(string='Audiencias')
# 	an_otro = fields.Char(string='Otro: ')
# 	an_marca = fields.Char(string='Marca o Producto*')
# 	an_sector = fields.Char(string='Sector (NIELSEN/IBOPE)*')
# 	an_categoria = fields.Char(string='Categoria (NIELSEN/IBOPE)*')
# 	an_year_inmediato = fields.Boolean(string='Año Inmediato Anterior')
# 	an_year_movil = fields.Boolean(string='Año Móvil')
# 	an_periodo = fields.Char(string='Otro Periodo')
# 	an_analisis = fields.Text(string='Objetivo del Análisis. En caso de requerir comparativo de marcas especificas, señalarlo.')
# 	an_year_inmediato1 = fields.Boolean(string='Año Inmediato Anterior')
# 	an_year_movil1 = fields.Boolean(string='Año Móvil')
# 	an_periodo1 = fields.Char(string='Otro Periodo')
# 	an_target_interes = fields.Char(string='Target de interés*')
# 	an_analisis1 = fields.Text(string='Objetivo del Análisis.')	
# 	an_marca1 = fields.Char(string='Categoría o Marca/Producto de interés*')
# 	an_target_interes1 = fields.Char(string='Target de interés*')
# 	an_analisis2 = fields.Text(string='Objetivo del Análisis. (¿Qué se desea conocer?)')
# 	an_tro_descripcion = fields.Text(string='Describir el tipo de análisisá y/o requerimientos de informacion.')
	# medios = fields.Monetary(string='Medios P. Autorizado')

	
	@api.model
	def create(self,vals):
		sequence = self.env['ir.sequence'].next_by_code('odt.medios')
		vals['name'] = sequence or 'Nuevo'
		return super(OdtMedios, self).create(vals)

class CanalesTags(models.Model):
	_name = 'canales.tags'

	name = fields.Char(string='Nombre')
		

	
class OdtContactcenter(models.Model):
	_name = 'odt.contactcenter'
	_description = 'Ventana kanban para la estructura de Contact Center'
	_inherit = ['mail.thread', 'mail.activity.mixin','crm.odt']


	# Contact Center
	cc_telefono = fields.Boolean(string='Teléfono', track_visibility=True)
	cc_whats = fields.Boolean(string='WhatsApp', track_visibility=True)
	cc_email = fields.Boolean(string='E-mail', track_visibility=True)
	cc_twitter = fields.Boolean(string='Twitter', track_visibility=True)
	cc_face = fields.Boolean(string='Facebook', track_visibility=True)
	cc_chat = fields.Boolean(string='Chat', track_visibility=True)
	cc_escritorio = fields.Boolean(string='Escritorio', track_visibility=True)
	cc_otro = fields.Boolean(string='Otro', track_visibility=True)
	cc_especificar = fields.Text(string='Especificar', track_visibility=True)

	tipo_servicio1 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', track_visibility=True)
	dictaminacion1 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes1 = fields.Boolean(string='Lunes', track_visibility=True)
	martes1 = fields.Boolean(string='Martes', track_visibility=True)
	miercoles1 = fields.Boolean(string='Miércoles', track_visibility=True)
	jueves1 = fields.Boolean(string='Jueves', track_visibility=True)
	viernes1 = fields.Boolean(string='Viernes', track_visibility=True)
	sabado1 = fields.Boolean(string='Sábado', track_visibility=True)
	domingo1 = fields.Boolean(string='Domingo', track_visibility=True)
	festivos1 = fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart1 = fields.Float(string='Hora inicial', track_visibility=True)
	atencionend1 = fields.Float(string='Hora Término', track_visibility=True)

	tipo_servicio2 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', track_visibility=True)
	dictaminacion2 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes2 = fields.Boolean(string='Lunes', track_visibility=True)
	martes2 = fields.Boolean(string='Martes', track_visibility=True)
	miercoles2= fields.Boolean(string='Miércoles', track_visibility=True)
	jueves2= fields.Boolean(string='Jueves', track_visibility=True)
	viernes2= fields.Boolean(string='Viernes', track_visibility=True)
	sabado2= fields.Boolean(string='Sábado', track_visibility=True)
	domingo2= fields.Boolean(string='Domingo', track_visibility=True)
	festivos2=fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart2= fields.Float(string='Hora inicial', track_visibility=True)
	atencionend2= fields.Float(string='Hora Término', track_visibility=True)
	tipo_servicio3 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', track_visibility=True)
	dictaminacion3 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes3= fields.Boolean(string='Lunes', track_visibility=True)
	martes3= fields.Boolean(string='Martes', track_visibility=True)
	miercoles3= fields.Boolean(string='Miércoles', track_visibility=True)
	jueves3= fields.Boolean(string='Jueves', track_visibility=True)
	viernes3= fields.Boolean(string='Viernes', track_visibility=True)
	sabado3= fields.Boolean(string='Sábado', track_visibility=True)
	domingo3= fields.Boolean(string='Domingo', track_visibility=True)
	festivos3= fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart3= fields.Float(string='Hora inicial', track_visibility=True)
	atencionend3= fields.Float(string='Hora Término', track_visibility=True)
	tipo_servicio4 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', track_visibility=True)
	dictaminacion4 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes4= fields.Boolean(string='Lunes', track_visibility=True)
	martes4= fields.Boolean(string='Martes', track_visibility=True)
	miercoles4= fields.Boolean(string='Miércoles', track_visibility=True)
	jueves4= fields.Boolean(string='Jueves', track_visibility=True)
	viernes4= fields.Boolean(string='Viernes', track_visibility=True)
	sabado4= fields.Boolean(string='Sábado', track_visibility=True)
	domingo4= fields.Boolean(string='Domingo', track_visibility=True)
	festivos4= fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart4= fields.Float(string='Hora inicial', track_visibility=True)
	atencionend4= fields.Float(string='Hora Término', track_visibility=True)
	tipo_servicio5 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', track_visibility=True)
	dictaminacion5 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes5= fields.Boolean(string='Lunes', track_visibility=True)
	martes5= fields.Boolean(string='Martes', track_visibility=True)
	miercoles5= fields.Boolean(string='Miércoles', track_visibility=True)
	jueves5= fields.Boolean(string='Jueves', track_visibility=True)
	viernes5= fields.Boolean(string='Viernes', track_visibility=True)
	sabado5= fields.Boolean(string='Sábado', track_visibility=True)
	domingo5= fields.Boolean(string='Domingo', track_visibility=True)
	festivos5= fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart5= fields.Float(string='Hora inicial', track_visibility=True)
	atencionend5= fields.Float(string='Hora Término', track_visibility=True)
	tipo_servicio6 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', track_visibility=True)
	dictaminacion6 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes6= fields.Boolean(string='Lunes', track_visibility=True)
	martes6= fields.Boolean(string='Martes', track_visibility=True)
	miercoles6= fields.Boolean(string='Miércoles', track_visibility=True)
	jueves6= fields.Boolean(string='Jueves', track_visibility=True)
	viernes6= fields.Boolean(string='Viernes', track_visibility=True)
	sabado6= fields.Boolean(string='Sábado', track_visibility=True)
	domingo6= fields.Boolean(string='Domingo', track_visibility=True)
	festivos6= fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart6= fields.Float(string='Hora inicial', track_visibility=True)
	atencionend6= fields.Float(string='Hora Término', track_visibility=True)

	tipo_servicio7 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', track_visibility=True)
	dictaminacion7 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes7= fields.Boolean(string='Lunes', track_visibility=True)
	martes7= fields.Boolean(string='Martes', track_visibility=True)
	miercoles7= fields.Boolean(string='Miércoles', track_visibility=True)
	jueves7= fields.Boolean(string='Jueves', track_visibility=True)
	viernes7= fields.Boolean(string='Viernes', track_visibility=True)
	sabado7= fields.Boolean(string='Sábado', track_visibility=True)
	domingo7= fields.Boolean(string='Domingo', track_visibility=True)
	festivos7= fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart7= fields.Float(string='Hora inicial', track_visibility=True)
	atencionend7= fields.Float(string='Hora Término', track_visibility=True)

	tipo_servicio8 = fields.Selection([('1','Atención'),('2','Registro'),('3','Atención y Registro'),
									   ('4','Validación de Documentos'),('5','Dictaminación'),('6','Otro')], string='Tipo de Servicio', track_visibility=True)
	dictaminacion8 = fields.Integer(string='Numero de Dictaminación', track_visibility=True)
	lunes8 = fields.Boolean(string='Lunes', track_visibility=True)
	martes8 = fields.Boolean(string='Martes', track_visibility=True)
	miercoles8 = fields.Boolean(string='Miércoles', track_visibility=True)
	jueves8 = fields.Boolean(string='Jueves', track_visibility=True)
	viernes8 = fields.Boolean(string='Viernes', track_visibility=True)
	sabado8 = fields.Boolean(string='Sábado', track_visibility=True)
	domingo8 = fields.Boolean(string='Domingo', track_visibility=True)
	festivos8 = fields.Boolean(string='¿Deben considerarse los dias festivos?', track_visibility=True)
	atencionstart8 = fields.Float(string='Hora inicial', track_visibility=True)
	atencionend8 = fields.Float(string='Hora Término', track_visibility=True)
	firma1_contact = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_contact = fields.Binary(string='Firma 2', track_visibility=True)
	contact_center = fields.Float(string='Contact Center P. Autorizado',track_visibility=True)
	tabla_cotizacion_contact1 = fields.One2many('odt.cotizacion.contact1','cotizacion_contact1_id')
	tabla_cotizacion_contact2 = fields.One2many('odt.cotizacion.contact2','cotizacion_contact2_id')
	tabla_cotizacion_contact3 = fields.One2many('odt.cotizacion.contact3','cotizacion_contact3_id')
	tabla_cotizacion_contact4 = fields.One2many('odt.cotizacion.contact4','cotizacion_contact4_id')

	
	@api.model
	def create(self,vals):
		sequence = self.env['ir.sequence'].next_by_code('odt.contactcenter')
		vals['name'] = sequence or 'Nuevo'
		return super(OdtContactcenter, self).create(vals)

class OdtBtlpdv(models.Model):
	_name = 'odt.btlpdv'
	_description = 'Ventana kanban para la estructura de BTL'
	_inherit = ['mail.thread', 'mail.activity.mixin','crm.odt']

	@api.depends('tabla_cotizacion_btl')
	def _btl_totales(self):
		self.total_precio_unitario_btl = sum(line.precio_unitario_btl for line in self.tabla_cotizacion_btl)
		self.total_costo_proveedor_btl = sum(line.costo_proveedor_btl for line in self.tabla_cotizacion_btl)
	
	# BTL/PDV
	activation = fields.Boolean(string='Activación', track_visibility=True)
	mystery_shopper = fields.Boolean(string='Mystery Shopper', track_visibility=True)
	promotoria = fields.Boolean(string='Promotoria', track_visibility=True)
	sumpling = fields.Boolean(string='Sampling', track_visibility=True)
	production_material = fields.Boolean(string='Producción de Materiales', track_visibility=True)
	production_promocionales = fields.Boolean(string='Producción de Promocionales', track_visibility=True)
	auto_servicio  = fields.Boolean(string='Auto Servicio', track_visibility=True)
	departament   = fields.Boolean(string='Departamentales', track_visibility=True)
	centro_comercial  = fields.Boolean(string='Centros Comerciales', track_visibility=True)
	calle  = fields.Boolean(string='Calles', track_visibility=True)
	otros  = fields.Boolean(string='Otros (Por favor detallar actividad)', track_visibility=True)
	others = fields.Text(string='Otros', track_visibility=True)
	vigencia = fields.Date(string='Vigencia', track_visibility=True)
	activ_days = fields.Integer(string='Dias a Activar', size='3', track_visibility=True)
	coverage = fields.Char(string='Cobertura', track_visibility=True)
	material_apoyo = fields.Text(string='Materiales de apoyo (Descripción y Cantidad)', track_visibility=True)
	comentarios_add = fields.Text(string='Comentarios Adicionales', track_visibility=True)
	listado_tiendas = fields.Text(string='Listado de Tiendas', track_visibility=True)
	btl = fields.Float(string='BTL/PDV P. Autorizado', track_visibility=True)
	firma1_btl = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_btl = fields.Binary(string='Firma 2', track_visibility=True)
	c_promocion = fields.Char(string='PROMOCIÓN: ', track_visibility=True)
	c_clave = fields.Char(string='CLAVE: ', track_visibility=True)
	c_fecha = fields.Date(string='FECHA: ', track_visibility=True)
	c_direccion = fields.Char(string='DIRECCIÓN: ', track_visibility=True)
	c_gerencia = fields.Char(string='GERENCIA: ', track_visibility=True)
	c_solicita = fields.Many2one('hr.employee',string='SOLICITA: ', track_visibility=True)
	c_proveedor = fields.Many2one('res.partner',string='PROVEEDOR: ', track_visibility=True)
	tabla_material_btl = fields.One2many('odt.materiales', 'material_id')
	tabla_cotizacion_btl = fields.One2many('odt.cotizacion','cotizacion_id')
	total_precio_unitario_btl = fields.Float(string='Total P. Unitario',compute=_btl_totales)
	total_costo_proveedor_btl = fields.Float(string='Total Proveedor',compute=_btl_totales)
	
	@api.model
	def create(self,vals):
		sequence = self.env['ir.sequence'].next_by_code('odt.btlpdv')
		vals['name'] = sequence or 'Nuevo'
		return super(OdtBtlpdv, self).create(vals)

class OdtDiseno(models.Model):
	_name = 'odt.diseno'
	_description = 'Ventana kanban para la estructura de Diseño'
	_inherit = ['mail.thread', 'mail.activity.mixin','crm.odt']

	
	@api.model
	def create(self,vals):
		sequence = self.env['ir.sequence'].next_by_code('odt.diseno')
		vals['name'] = sequence or 'Nuevo'
		return super(OdtDiseno, self).create(vals)

	@api.depends('tabla_cotizacion_diseno')
	def _diseno_totales(self):
		self.total_cliente_diseno = sum(line.costo_cliente for line in self.tabla_cotizacion_diseno)
		self.total_gtvo_diseno = sum(line.precio_uni_gtvp for line in self.tabla_cotizacion_diseno)
		self.total_terceros_diseno = sum(line.pago_terceros for line in self.tabla_cotizacion_diseno)
		self.total_interno_diseno = sum(line.costo_interno for line in self.tabla_cotizacion_diseno)
		self.total_recuperacion_diseno = sum(line.recuperacion for line in self.tabla_cotizacion_diseno)

	# Diseño 
	d_presentacion = fields.Boolean(string='Presentación', track_visibility=True)
	d_template = fields.Boolean(string='Template', track_visibility=True)
	d_master_graph = fields.Boolean(string='MasterGraphic', track_visibility=True)
	d_adaptacion_pop = fields.Boolean(string='Adaptacion a POP', track_visibility=True)
	d_adaptacion_digital = fields.Boolean(string='Adaptación a Digital', track_visibility=True)
	d_adaptacion_ooh = fields.Boolean(string='Adaptación a OOH', track_visibility=True)
	d_logotipo = fields.Boolean(string='Logotipo', track_visibility=True)
	d_visualizacion = fields.Boolean(string='Visualización', track_visibility=True)
	d_otro = fields.Boolean(string='Otros', track_visibility=True)
	d_otro_desc = fields.Text(string='Especificar', track_visibility=True)
	dc_especificacion = fields.Text(string='Comentarios y especificaciones', track_visibility=True)
	firma1_design = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_design = fields.Binary(string='Firma 2', track_visibility=True)
	diseño_creatividad = fields.Float(string='Diseño P. Autorizado', track_visibility=True)
	tabla_material_diseno = fields.One2many('odt.materiales.diseno', 'material_diseno_id')
	tabla_cotizacion_diseno = fields.One2many('odt.cotizacion.diseno','cotizacion_diseno_id')
	total_cliente_diseno = fields.Float(string='Total Cliente',compute=_diseno_totales)
	total_gtvo_diseno = fields.Float(string='Total GTVP',compute=_diseno_totales)
	total_terceros_diseno = fields.Float(string='Total Terceros',compute=_diseno_totales)
	total_interno_diseno = fields.Float(string='Total Interno',compute=_diseno_totales)
	total_recuperacion_diseno = fields.Float(string='Total Recuperacion',compute=_diseno_totales)

class OdtGestoria(models.Model):
	_name = 'odt.gestoria'
	_description = 'Ventana kanban para Gestoria'
	_inherit = ['mail.thread', 'mail.activity.mixin','crm.odt']

	
	@api.model
	def create(self,vals):
		sequence = self.env['ir.sequence'].next_by_code('odt.gestoria')
		vals['name'] = sequence or 'Nuevo'
		return super(OdtGestoria, self).create(vals)

	@api.depends('tabla_cotizacion_gestoria')
	def _gestoria_totales(self):
		self.total_cliente_gestoria = sum(line.costo_cliente for line in self.tabla_cotizacion_gestoria)
		self.total_terceros_gestoria = sum(line.pago_terceros for line in self.tabla_cotizacion_gestoria)
		self.total_precio = sum(line.precio_total for line in self.tabla_cotizacion_gestoria)

	# 	 Gestoria
	gl_date_sorteo = fields.Text(string='Fecha del Sorteo', track_visibility=True)
	site_sorteo = fields.Text(string='Lugar del Sorteo', track_visibility=True)
	description_premio = fields.Text(string='b) Descripción', track_visibility=True)
	description_by_premio = fields.Integer(string='a) Cantidad', track_visibility=True)
	valor_primio = fields.Float(string='c) Valor unitario', track_visibility=True)
	lugar_enterga_premio = fields.Text(string='Lugar de entrega del premio', track_visibility=True)
	dates_hrs_entrega = fields.Text(string='Fecha(s) y horario(s) de entrega de premios', track_visibility=True)
	responsable_promo = fields.Char(string='Responsable de la promocion', track_visibility=True)
	dl_comments = fields.Text(string='Comentarios adicionales', track_visibility=True)
	clave_proyecto = fields.Char(string='Clave del Proyecto', track_visibility=True)
	social_reason = fields.Char(string='Razon Social', track_visibility=True)
	respons_promocion = fields.Many2one('res.partner', string='Responsable de la Promocion', track_visibility=True)
	respons_trato_personal = fields.Many2one('hr.employee',string='Resposnsable de tratamiento de datos personales', track_visibility=True)
	name_promo = fields.Char(string='Nombre de la Promocion', track_visibility=True)
	geo_cobertura = fields.Char(string='Cobertura Geografica', track_visibility=True)
	vigencia_promo = fields.Char(string='Vigencia de la promocion', track_visibility=True)
	promotion = fields.Selection([('1','Sorteo'),('2','Concurso'),('3','RTC'),('4','Canje / Coleccionable'),('5','Otra')],string='Tipo de promoción')
	# dl_sorteo = fields.Boolean(string='', track_visibility=True)
	# gl_concurso = fields.Boolean(string='', track_visibility=True)
	# gr_rtc = fields.Boolean(string='RTC', track_visibility=True)
	# gl_canje = fields.Boolean(string='Canje / Coleccionable', track_visibility=True)
	# gl_otra = fields.Boolean(string='Otra', track_visibility=True)
	gl_vigencia_permiso = fields.Date(string='Vigencia del Permiso:', track_visibility=True)
	gl_talon_boleto = fields.Boolean(string='Talon / Boleto', track_visibility=True)
	gl_electr_boleto = fields.Boolean(string='Boleto electronico', track_visibility=True)
	gl_formacion_num = fields.Boolean(string='Formacion de Numeros', track_visibility=True)
	gl_sistema_info = fields.Boolean(string='Sistema Informatico "Random"', track_visibility=True)
	gl_sorteo_insta = fields.Boolean(string='Sorteo Instantaneo', track_visibility=True)
	gl_cal_gana = fields.Boolean(string='Calcula y Gana', track_visibility=True)
	gl_predeterminado = fields.Boolean(string='Predeterminado', track_visibility=True)
	gl_juego_linea = fields.Boolean(string='Juego en Linea', track_visibility=True)
	gl_mayor_puntaje = fields.Boolean(string='Mayor Puntaje', track_visibility=True)
	gl_con_otro = fields.Boolean(string='Otro', track_visibility=True)
	gl_dec_otro = fields.Text(string='Otro periodico')

	gl_talon_calcula = fields.Boolean(string='Calcula y gana')
	gl_juego_linea_concurso = fields.Boolean(string='Juego en línea con tiempo')
	gl_creatividad_p = fields.Boolean(string='Creatividad de participante')
	gl_acumulacion_p = fields.Boolean(string='Acumulación de puntos')
	gl_acomulacion_compra = fields.Boolean(string='Acumulación de pruebas de compra')
	gl_subasta = fields.Boolean(string='Subasta')	
	gl_otra = fields.Boolean(string='Otra')

	total_premios = fields.Text(string='Valor total de Premios')
	cert_foios = fields.Boolean(string='Llenado de Urnas', track_visibility=True)
	det_ganadores = fields.Boolean(string='Determinacion de Ganadores', track_visibility=True)
	entrega_premio = fields.Boolean(string='Entrega de premios', track_visibility=True)
	gl_mecanica = fields.Text(string='Mecanica de participación', track_visibility=True)
	universal = fields.Boolean(string='Universal', track_visibility=True)
	excelsior = fields.Boolean(string='Excelsior', track_visibility=True)
	novedades = fields.Boolean(string='Novedades', track_visibility=True)
	la_prensa = fields.Boolean(string='La Prensa', track_visibility=True)
	el_record = fields.Boolean(string='El Record', track_visibility=True)
	publimetro = fields.Boolean(string='Publimetro', track_visibility=True)
	esto = fields.Boolean(string='Esto', track_visibility=True)
	jornada = fields.Boolean(string='La Jornada', track_visibility=True)
	gl_preiodico_otros = fields.Boolean(string='Otros', track_visibility=True)
	pagina_web = fields.Char(string='Pagina Web', track_visibility=True)
	gl_observations = fields.Text(string='Observaciones', track_visibility=True)
	no_sorteo = fields.Integer(string='Numero de Sorteos',size='2', requiered=True)
	tabla_cotizacion_gestoria = fields.One2many('odt.cotizacion.gestoria','cotizacion_gestoria_id', track_visibility=True)
	total_cliente_gestoria = fields.Float(string='Total Cliente',compute=_gestoria_totales)
	total_terceros_gestoria = fields.Float(string='Total Terceros',compute=_gestoria_totales)
	total_precio = fields.Float(string='Suma total costo venta al cliente', compute=_gestoria_totales)
	gestoria = fields.Float(string='Gestoria P. Autorizado', track_visibility=True)
	firma1_gestoria = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_gestoria = fields.Binary(string='Firma 2', track_visibility=True)

class OdtProduccion(models.Model):
	_name = 'odt.produccion'
	_description = 'Ventana kanban para Producción'
	_inherit = ['mail.thread', 'mail.activity.mixin','crm.odt']

	@api.model
	def create(self,vals):
		sequence = self.env['ir.sequence'].next_by_code('odt.produccion')
		vals['name'] = sequence or 'Nuevo'
		return super(OdtProduccion, self).create(vals)

	@api.depends('tabla_cotizacion_produccion')
	def _produccion_totales(self):
		self.total_cliente_produ = sum(line.costo_cliente for line in self.tabla_cotizacion_produccion)
		self.total_gtvo_produ = sum(line.precio_uni_gtvp for line in self.tabla_cotizacion_produccion)
		self.total_terceros_produ = sum(line.pago_terceros for line in self.tabla_cotizacion_produccion)
		self.total_interno_produ = sum(line.costo_interno for line in self.tabla_cotizacion_produccion)
		self.total_recuperacion_produ = sum(line.recuperacion for line in self.tabla_cotizacion_produccion)

	# Produccion
	p_spot_radio = fields.Boolean(string='Spot Radio', track_visibility=True)
	p_spot_tv = fields.Boolean(string='Spot TV (Live Action)', track_visibility=True)
	p_spot_tv1 = fields.Boolean(string='Spot TV (Mtion Graphics)', track_visibility=True)
	p_cap_digital = fields.Boolean(string='Cápsula Digital', track_visibility=True)
	p_cineminuto = fields.Boolean(string='Video', track_visibility=True)
	p_lev_imagen = fields.Boolean(string='Cpsula / Mencin', track_visibility=True)
	p_pieca = fields.Boolean(string='Jingle', track_visibility=True)
	p_super = fields.Boolean(string='Video Corporativo', track_visibility=True)
	p_shooting_photo = fields.Boolean(string='Inclusion de Grafico', track_visibility=True)
	p_edicion_video = fields.Boolean(string='Inclusion de super', track_visibility=True)
	p_post_video = fields.Boolean(string='Otro', track_visibility=True)
	p_cortinilla = fields.Boolean(string='Duracion', track_visibility=True)
	p_reel = fields.Boolean(string='Descripcion', track_visibility=True)
	p_render = fields.Boolean(string='Render', track_visibility=True)
	p_locucion = fields.Boolean(string='Locución o Música', track_visibility=True)
	p_edicion_audio = fields.Boolean(string='Edición de Video', track_visibility=True)
	p_gif = fields.Boolean(string='Gif', track_visibility=True)
	p_ftp = fields.Boolean(string='FTP Especificaciones', track_visibility=True)
	p_otros = fields.Boolean(string='Otros', track_visibility=True)
	p_otro_text = fields.Text(string='Otros', track_visibility=True)
	p_duracion = fields.Char(string='Duración', track_visibility=True)
	descripcion = fields.Text(string='Descripción', track_visibility=True)
	tipo_trabajo = fields.Selection([('1','Proyecto Cobrado'),('2','Proyecto Bonificado'),('3','Proyecto a Cotizar')], track_visibility=True)
	firma1_prod = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_prod = fields.Binary(string='Firma 2', track_visibility=True)
	produccion = fields.Float(string='Produccion P. Autorizado', track_visibility=True)
	tabla_material_produccion = fields.One2many('odt.materiales.produccion', 'material_produccion_id')
	tabla_cotizacion_produccion = fields.One2many('odt.cotizacion.produccion','cotizacion_produccion_id')
	total_cliente_produ = fields.Float(string='Total Cliente',compute=_produccion_totales)
	total_gtvo_produ = fields.Float(string='Total GTVP',compute=_produccion_totales)
	total_terceros_produ = fields.Float(string='Total Terceros',compute=_produccion_totales)
	total_interno_produ = fields.Float(string='Total Interno',compute=_produccion_totales)
	total_recuperacion_produ = fields.Float(string='Total Recuperacion',compute=_produccion_totales)

class OdtMarketingDigital(models.Model):
	_name = 'odt.digital'
	_description = 'Ventana kanban para Digital'
	_inherit = ['mail.thread', 'mail.activity.mixin','crm.odt']

	@api.model
	def create(self,vals):
		sequence = self.env['ir.sequence'].next_by_code('odt.digital')
		vals['name'] = sequence or 'Nuevo'
		return super(OdtMarketingDigital, self).create(vals)

	@api.depends('tabla_cotizacion_digital')
	def _digital_totales(self):
		self.total_costo_interno_digital = sum(line.costo_interno for line in self.tabla_cotizacion_digital)
		self.total_pago_terceros_digital = sum(line.pago_terceros for line in self.tabla_cotizacion_digital)
		self.total_recuperacion_digital= sum(line.recuperacion for line in self.tabla_cotizacion_digital)
		self.total_costo_cliente_digital = sum(line.costo_cliente for line in self.tabla_cotizacion_digital)
		self.total_monto_venta_digital = sum(line.monto_venta for line in self.tabla_cotizacion_digital)

	# 	 Marketing Digital
	dg_web = fields.Boolean(string='Pagina web / micrositio', track_visibility=True)
	dg_galeria_video = fields.Boolean(string='Galeria de Videos', track_visibility=True)
	dg_descr = fields.Text(string='Descripcion General', track_visibility=True)
	dg_aplications = fields.Boolean(string=' Video Juego / aplicacion', track_visibility=True)
	dg_social_net = fields.Boolean(string='Redes sociales', track_visibility=True)
	dg_pautadg = fields.Boolean(string='Pauta digital', track_visibility=True)
	dg_promoweb = fields.Boolean(string='Promoweb', track_visibility=True)
	dg_estrategi = fields.Boolean(string='Estrategia', track_visibility=True)
	dg_mantenimiento = fields.Boolean(string='Mantenimiento Mensual', track_visibility=True)
	dg_galeria = fields.Boolean(string='Galeria de fotos', track_visibility=True)
	dg_camara = fields.Boolean(string='Camara en vivo', track_visibility=True)
	dg_calendar = fields.Boolean(string='Calendario', track_visibility=True)
	dg_otro = fields.Boolean(string='Otro', track_visibility=True)
	dg_otro_detalle = fields.Text(string='Detallar', track_visibility=True)
	dg_sistema_votacion = fields.Boolean(string='Sistema de votacion', track_visibility=True)
	dg_registro = fields.Boolean(string='Registro de participacion', track_visibility=True)
	dg_newsletter = fields.Boolean(string='Newsletter', track_visibility=True)
	dg_trivias = fields.Boolean(string='Trivias', track_visibility=True)
	dg_aplications_realtime = fields.Boolean(string='Aplicacion de reportes en tiempo real', track_visibility=True)
	dg_descripcion_va = fields.Text(string='Descripcion', track_visibility=True)
	n_niveles = fields.Integer(string='Numero de niveles', track_visibility=True)
	dg_opt_1 = fields.Boolean(string='Animacion 2D', track_visibility=True)
	dg_opt_2 = fields.Boolean(string='Animacion 3D', track_visibility=True)
	dg_opt_3 = fields.Boolean(string='Plataforma IOS', track_visibility=True)
	dg_opt_4 = fields.Boolean(string='Plataforma Android', track_visibility=True)
	dg_opt_5 = fields.Boolean(string='Plataforma Sitio web', track_visibility=True)
	dg_opt_6 = fields.Boolean(string='Plataforma Facebook', track_visibility=True)
	dg_opt_7 = fields.Boolean(string='Facebook', track_visibility=True)
	dg_opt_8 = fields.Boolean(string='Youtube', track_visibility=True)
	dg_opt_9 = fields.Boolean(string='Linked in', track_visibility=True)
	dg_opt_10 = fields.Boolean(string='Foursquare', track_visibility=True)
	dg_opt_11 = fields.Boolean(string='Twitter', track_visibility=True)
	dg_opt_12 = fields.Boolean(string='Pinterest', track_visibility=True)
	dg_opt_13 = fields.Boolean(string='Instagram', track_visibility=True)
	dg_opt_14 = fields.Boolean(string='Otros', track_visibility=True)
	dg_propuesta = fields.Text(string='Propuestas', track_visibility=True)
	dg_presupuesto = fields.Char(string='Presupuesto', track_visibility=True)
	dg_objetivos = fields.Char(string='Objeticos', track_visibility=True)
	dg_alcance = fields.Char(string='Alcance', track_visibility=True)
	dg_banner = fields.Char(string='Banners', track_visibility=True)
	dg_observations = fields.Char(string='Observaciones', track_visibility=True)
	dg_opt_15 = fields.Boolean(string='Banner Principal', track_visibility=True)
	dg_opt_16 = fields.Boolean(string='Banner Secundario', track_visibility=True)
	dg_opt_17 = fields.Boolean(string='Contenidos Editoriales', track_visibility=True)
	dg_opt_18 = fields.Boolean(string='Promocion', track_visibility=True)
	dg_opt_19 = fields.Boolean(string='E-mailing', track_visibility=True)
	dg_opt_20 = fields.Boolean(string='Dominio', track_visibility=True)
	dg_opt_21 = fields.Boolean(string='Hosting', track_visibility=True)
	dg_opt_22 = fields.Boolean(string='Otro', track_visibility=True)
	dg_sub_detalle = fields.Boolean(string='Detalle', track_visibility=True)
	dg_opt_23 = fields.Boolean(string='Sistema Random', track_visibility=True)
	dg_opt_24 = fields.Boolean(string='Generacion de codigos Unicos', track_visibility=True)
	dg_cant_codigos = fields.Integer(string='Cantidad de Codigos', track_visibility=True)
	dg_cant_digitos = fields.Integer(string='Cantidad de Digitos', track_visibility=True)
	dg_opt_25 = fields.Boolean(string='Numericos', track_visibility=True)
	dg_opt_26 = fields.Boolean(string='Alfa numericos', track_visibility=True)
	dg_otros = fields.Text(string='Otro', track_visibility=True)
	firma1_digital = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_digital = fields.Binary(string='Firma 2', track_visibility=True)
	digital = fields.Float(string='Marketing Digital P. Autorizado')

	tabla_cotizacion_digital = fields.One2many('odt.cotizacion.digital','cotizacion_digital_id')
	total_costo_interno_digital = fields.Float(string='Costo total interno',compute=_digital_totales)
	total_pago_terceros_digital = fields.Float(string='Pago a Terceros',compute=_digital_totales)
	total_recuperacion_digital = fields.Float(string='Recuperacion',compute=_digital_totales)
	total_costo_cliente_digital = fields.Float(string='Costo Cliente',compute=_digital_totales)
	total_monto_venta_digital = fields.Float(string='Monto de Venta',compute=_digital_totales)

class OdtLogistica(models.Model):
	_name = 'odt.logistica'
	_description = 'Ventana kanban para Logistica'
	_inherit = ['mail.thread', 'mail.activity.mixin','crm.odt']

	@api.model
	def create(self,vals):
		sequence = self.env['ir.sequence'].next_by_code('odt.logistica')
		vals['name'] = sequence or 'Nuevo'
		return super(OdtLogistica, self).create(vals)

	@api.depends('tabla_cotizacion_logistica')
	def _logistica_totales(self):
		self.total_cliente_logistica = sum(line.costo_cliente for line in self.tabla_cotizacion_logistica)
		self.total_venta_cliente_logistica = sum(line.costo_venta_cliente for line in self.tabla_cotizacion_logistica)
		self.total_terceros_logistica = sum(line.pago_terceros for line in self.tabla_cotizacion_logistica)

	#Logistica
	wiz_oport_id = fields.Many2one('crm.lead', 'Opportunity')
	tipo_promo = fields.Selection([('1','SEGOB'),('2','PROFECTO'),('3','RTC')], string='Tipo de promoción', track_visibility=True)
	mecanica_partici = fields.Text(string='Mecánica de participación', track_visibility=True)	
	total_ganador = fields.Char(string='Total ganadores', track_visibility=True)
	total_premio = fields.Char(string='Total Premios', track_visibility=True)
	total_ganador_premio = fields.Char(string='Total ganadores por tipo de premio', track_visibility=True)
	valor_premio = fields.Char(string='Valor de premios', track_visibility=True)
	caract_premio = fields.Text(string='Domensiones y pesos de premios', track_visibility=True)
	vigencia_promo = fields.Date(string='Vigencia de la promoción', track_visibility=True)
	geo_cobertura = fields.Text(string='Cobertura Geografica', track_visibility=True)

	tabla_cotizacion_logistica = fields.One2many('odt.cotizacion.logistica','cotizacion_logistica_id')	
	total_cliente_logistica = fields.Float(string='Total Cliente',compute=_logistica_totales)
	total_venta_cliente_logistica = fields.Float(string='Total GTVP',compute=_logistica_totales)
	total_terceros_logistica = fields.Float(string='Total Terceros',compute=_logistica_totales)
	firma1_logistica = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_logistica = fields.Binary(string='Firma 2', track_visibility=True)

class OdtEstrategia(models.Model):
	_name = 'odt.estrategia'
	_description = 'Ventana kanban para Estrategia'
	_inherit = ['mail.thread', 'mail.activity.mixin','crm.odt']

	@api.model
	def create(self,vals):
		sequence = self.env['ir.sequence'].next_by_code('odt.estrategia')
		vals['name'] = sequence or 'Nuevo'
		return super(OdtEstrategia, self).create(vals)
		

	@api.depends('tabla_cotizacion_estrategia')
	def _estrategia_totales(self):
		self.total_cliente_estrategia = sum(line.costo_cliente for line in self.tabla_cotizacion_estrategia)
		self.total_gtvo_estrategia = sum(line.precio_uni_gtvp for line in self.tabla_cotizacion_estrategia)
		self.total_terceros_estrategia = sum(line.pago_terceros for line in self.tabla_cotizacion_estrategia)
		self.total_interno_estrategia = sum(line.costo_interno for line in self.tabla_cotizacion_estrategia)
		self.total_recuperacion_estrategia = sum(line.recuperacion for line in self.tabla_cotizacion_estrategia)

	#Estrategia
	e_conc_promo = fields.Boolean(string='Concepto Promocional', track_visibility=True)
	e_conc_camp = fields.Boolean(string='Concepto de Campaña', track_visibility=True)
	e_mec_promv = fields.Boolean(string='Mecánica Promocional', track_visibility=True)
	e_estr_difu = fields.Boolean(string='Estrategia de Difusión', track_visibility=True)
	e_guion_r20 = fields.Boolean(string='Guión spot radio 20"', track_visibility=True)
	e_guion_r30 = fields.Boolean(string='Guión spot radio 30"', track_visibility=True)
	e_guion_10 = fields.Boolean(string='Guión spot radio 10"', track_visibility=True)
	e_guion_cineminuto = fields.Boolean(string='Guión Cineminuto', track_visibility=True)
	e_guion_capsula = fields.Boolean(string='Guión cápsula Tv/Web', track_visibility=True)
	e_copy = fields.Boolean(string='Copy', track_visibility=True)
	e_slogan = fields.Boolean(string='Slogan', track_visibility=True)
	e_naming = fields.Boolean(string='Naming', track_visibility=True)
	e_mailing = fields.Boolean(string='Mailing', track_visibility=True)
	e_creat_BTL = fields.Boolean(string='Creatividad BTL', track_visibility=True)
	e_concept = fields.Boolean(string='Concepto de eventos', track_visibility=True)
	e_otros = fields.Boolean(string='Otros', track_visibility=True)
	e_otro_text = fields.Text(string='Especificar', track_visibility=True)
	e_more_details = fields.Text(string='Mas Detalles', track_visibility=True)
	estrategia = fields.Float(string='Estrategia P. Autorizado', track_visibility=True)
	firma1_estrategia = fields.Binary(string='Firma 1', track_visibility=True)
	firma2_estrategia = fields.Binary(string='Firma 2', track_visibility=True)
	tabla_cotizacion_estrategia = fields.One2many('odt.cotizacion.estrategia','cotizacion_estrat_id')	
	total_cliente_estrategia = fields.Float(string='Total Cliente',compute=_estrategia_totales)
	total_gtvo_estrategia = fields.Float(string='Total GTVP',compute=_estrategia_totales)
	total_terceros_estrategia = fields.Float(string='Total Terceros',compute=_estrategia_totales)
	total_interno_estrategia = fields.Float(string='Total Interno',compute=_estrategia_totales)
	total_recuperacion_estrategia = fields.Float(string='Total Recuperacion',compute=_estrategia_totales)

# tablas one2many

class MaterialesBTL(models.Model):
	_name = 'odt.materiales'

	material_id = fields.Many2one("odt.btlpdv",ondelete='cascade')
	quantity = fields.Integer(string='Cantidad')
	tipo_material = fields.Selection([('1','Demostradora'),('2','Demo edecán'),('3','Promotor'),('4','Animador'),('5','Edecán A'),
									 ('6','Edecán AA'),('7','Edecán AAA'),('8','Gio A'),('9','Gio AA'),('10','Gio AAA'),('11','Modelos'),
									 ('12','Otros')],string='Tipo Material')
	medidas_formatos = fields.Char(string='Medidas / formatos')

class MaterialesDiseno(models.Model):
	_name = 'odt.materiales.diseno'

	material_diseno_id = fields.Many2one("odt.diseno",ondelete='cascade')
	tipo_material = fields.Char(string='Tipo de Material')
	medidas = fields.Char(string='Medidas')
	formatos = fields.Char(string='Formatos')

class MaterialesProduccion(models.Model):
	_name = 'odt.materiales.produccion'

	material_produccion_id = fields.Many2one("odt.produccion",ondelete='cascade')
	quantity = fields.Integer(string='Cantidad')
	tipo_material = fields.Char(string='Especificaciones de Material')
	medidas_formatos = fields.Char(string='Medidas / formatos / duracion')

class CotizacionesGestoria(models.Model):
	_name = 'odt.cotizacion.gestoria'
		
	cotizacion_gestoria_id = fields.Many2one('odt.gestoria', ondelete='cascade')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	precio_uni_gtvp = fields.Float(string='Precio unitario')
	precio_total = fields.Float(string='Precio Total', compute='precio_total_gesto')
	costo_cliente = fields.Float(string='Costo sugerido para cliente')
	pago_terceros = fields.Float(string='Pago a Terceros')
	costo_venta_cliente = fields.Float(string='Costo venta cliente*')

	@api.one
	@api.depends('cantidad','precio_uni_gtvp')
	def precio_total_gesto(self):
		self.precio_total = (self.cantidad * self.precio_uni_gtvp)		

class CotizacionesLogistica(models.Model):
	_name = 'odt.cotizacion.logistica'
		
	cotizacion_logistica_id = fields.Many2one('odt.logistica', ondelete='cascade')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	precio_unitario = fields.Float(string='Precio unitario')
	costo_cliente = fields.Float(string='Costo sugerido para cliente')
	pago_terceros = fields.Float(string='Pago a Terceros')
	costo_venta_cliente = fields.Float(string='Costo venta cliente*')		

class CotizacionesDigital(models.Model):
	_name = 'odt.cotizacion.digital'
		
	cotizacion_digital_id = fields.Many2one('odt.digital', ondelete='cascade')
	concepto = fields.Char(string='Concepto')
	periodo = fields.Char(string='Periodicidad')
	cantidad = fields.Integer(string='Cantidad')
	meses = fields.Char(string='Meses')
	horas = fields.Integer(string='Horas de servicio')
	costo_hora = fields.Float(string='Costo por Hora')
	costo_interno = fields.Float(string='*Costo Interno', compute='_costo_interno')
	pago_terceros = fields.Float(string='*Pago a Terceros')
	recuperacion = fields.Float(string='*Costo minimo de recuperacion')
	costo_cliente = fields.Float(string='*Costo Cliente')
	monto_venta = fields.Float(string='*Monto de Venta')

	@api.depends('horas','costo_hora','costo_interno')
	def _costo_interno(self):
		self.costo_interno = (self.costo_hora * self.horas )

class CotizacionesProduccion(models.Model):
	_name = 'odt.cotizacion.produccion'
		
	cotizacion_produccion_id = fields.Many2one('odt.produccion',ondelete='cascade')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	dias = fields.Integer(string='Dias')
	precio_uni_cliente = fields.Float(string='Precio Unitario Cliente')
	costo_cliente = fields.Float(string='*Costo Cliente')
	precio_uni_gtvp = fields.Float(string='Precio unitario GTVP')
	pago_terceros = fields.Float(string='*Pago a Terceros')
	costo_interno = fields.Float(string='*Costo Interno')
	recuperacion = fields.Float(string='Costo minimo de recuperacion')

	@api.one
	@api.depends('cantidad','dias','costo_cliente','precio_uni_cliente')
	def _costo_cliente(self):
		self.costo_cliente = self.precio_uni_cliente * self.cantidad * self.dias


	@api.one
	@api.depends('cantidad','dias','pago_terceros','precio_uni_gtvp')
	def _pago_terceros(self):
		self.pago_terceros = self.precio_uni_gtvp  * self.cantidad * self.dias


	@api.one
	@api.depends('costo_interno','pago_terceros','recuperacion')
	def _pago_recuperacion(self):
		self.recuperacion = self.pago_terceros + self.costo_interno

class CotizacionesEstategia(models.Model):
	_name = 'odt.cotizacion.estrategia'
		
	cotizacion_estrat_id = fields.Many2one('odt.estrategia', ondelete='cascade')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	dias = fields.Integer(string='Dias')
	precio_uni_cliente = fields.Float(string='Precio Unitario Cliente')
	costo_cliente = fields.Float(string='*Costo Cliente')
	precio_uni_gtvp = fields.Float(string='Precio unitario GTVP')
	pago_terceros = fields.Float(string='*Pago a Terceros')
	costo_interno = fields.Float(string='*Costo Interno')
	recuperacion = fields.Float(string='Costo minimo de recuperacion')

class CotizacionesBTL(models.Model):
	_name = 'odt.cotizacion'
		
	cotizacion_id = fields.Many2one('odt.btlpdv')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	dias = fields.Integer(string='Dias')
	semanas = fields.Integer(string='Semanas')
	precio_unitario_btl = fields.Float(string='Precio Unitario')
	costo_proveedor_btl = fields.Float(string='Costo Proveedor', compute='_costo_provedor')

	@api.one
	@api.depends('cantidad','dias','semanas','precio_unitario_btl','costo_proveedor_btl')
	def _costo_provedor(self):
		self.costo_proveedor_btl = (self.cantidad * self.dias * self.semanas) * self.precio_unitario_btl

class CotizacionesContactcenter1(models.Model):
	_name = 'odt.cotizacion.contact1'

	cotizacion_contact1_id = fields.Many2one('odt.contactcenter', ondelete='cascade')
	tipo_llamada = fields.Selection([('1','Localización con dictamen de Ganador'),('2','Localización con dictamen de Respuesta Incorrecta'),('3','Intentos de localización con audio abierto para pasar a otro Ganador')],string='Tipo de llamada')
	costo_tvp = fields.Float(string='Costo TVP')
	costo_sugerido = fields.Float(string='Costo Sugerido al Cliente')
	information = fields.Float(string='Información que debe ser llenada por el área comercial una vez autorizado el proyecto')

class CotizacionesContactcenter2(models.Model):
	_name = 'odt.cotizacion.contact2'

	cotizacion_contact2_id = fields.Many2one('odt.contactcenter', ondelete='cascade')
	numero_dictaminacion = fields.Integer(string='Número de dictaminación')
	tipo_llamada = fields.Selection([('1','Localización con dictamen de Ganador'),('2','Localización con dictamen de Respuesta Incorrecta'),('3','Intentos de localización con audio abierto para pasar a otro Ganador')],string='Tipo de llamada')
	costo_unit_minimo_tvp = fields.Float(string='Costo Unitario minimo TVP')
	costo_total_minimo_tvp = fields.Float(string='Costo Unitario total TVP')
	costo_unit_minimo_cliente = fields.Float(string='Costo Unitario minimo cliente')
	costo_total_minimo_cliente = fields.Float(string='Costo Unitario minimo cliente')
	costo_unitario_cliente = fields.Float(string='Costo unitario al cliente')
	costo_total = fields.Float(string='Costo Total')

class CotizacionesContactcenter3(models.Model):
	_name = 'odt.cotizacion.contact3'

	cotizacion_contact3_id = fields.Many2one('odt.contactcenter', ondelete='cascade')
	numero_dictaminacion = fields.Integer(string='Número de dictaminación')
	tipo_llamada = fields.Selection([('1','Localización con dictamen de Ganador'),('2','Localización con dictamen de Respuesta Incorrecta'),('3','Intentos de localización con audio abierto para pasar a otro Ganador')],string='Tipo de llamada')
	costo_unit_minimo_tvp = fields.Float(string='Costo Unitario minimo TVP')
	costo_total_minimo_tvp = fields.Float(string='Costo Unitario total TVP')
	costo_unit_minimo_cliente = fields.Float(string='Costo Unitario minimo cliente')
	costo_total_minimo_cliente = fields.Float(string='Costo Unitario minimo cliente')
	costo_unitario_cliente = fields.Float(string='Costo unitario al cliente')
	costo_total = fields.Float(string='Costo Total')	

class CotizacionesContactcenter4(models.Model):
	_name = 'odt.cotizacion.contact4'

	cotizacion_contact4_id = fields.Many2one('odt.contactcenter', ondelete='cascade')
	llamada_salida = fields.Selection([('1','Llamada local y larga distancia nacional'),('2','Celular local y celular nacional')],string='Llamadas de salida')
	costo_minutio = fields.Float(string='Costo por minuto TVP')
	costo_minuto_sugerido = fields.Float(string='Costo por minuto sugerido')
	costo_minuto_vendido = fields.Float(string='Costo por minuto vendido')	

class CotizacionesDiseno(models.Model):
	_name = 'odt.cotizacion.diseno'
		
	cotizacion_diseno_id = fields.Many2one('odt.diseno', ondelete='cascade')
	concepto = fields.Char(string='Concepto')
	cantidad = fields.Integer(string='Cantidad')
	dias = fields.Integer(string='Dias')
	precio_uni_cliente = fields.Float(string='Precio Unitario Cliente')
	costo_cliente = fields.Float(string='*Costo Cliente')
	precio_uni_gtvp = fields.Float(string='Precio unitario GTVP')
	pago_terceros = fields.Float(string='*Pago a Terceros')
	costo_interno = fields.Float(string='*Costo Interno')
	recuperacion = fields.Float(string='Costo minimo de recuperacion')

class TablaPrensa(models.Model):
	_name = 'odt.medios.prensa'

	prensa_id = fields.Many2one('odt.medios')
	plaza = fields.Char(string='Plaza')
	titulo = fields.Char(string='Título')
	tamano = fields.Selection([('1','Plana'),('2','Robaplana'),('3','1/2 Plana Horizontal'),
							   ('4','1/2 Plana Vertical'),('5','1/4 Plana'),('6','1/8 Plana'),('7','Otro')],string='Tamaño')
	otro = fields.Char(string='Otros')
	seccion = fields.Char(string='Sección')
	fecha_publicacion = fields.Date(string='Fecha de Publicación')
	posicion = fields.Char(string='Posición')
	color = fields.Char(string='Color')

class TablaOoh(models.Model):
	_name = 'odt.medios.ooh'

	ooh_id = fields.Many2one('odt.medios')
	plaza = fields.Char(string='Plaza*')
	tipo_exterior = fields.Char(string='Típo de exterior*')
	observaciones = fields.Char(string='Observaciones')

class TablaRevista(models.Model):
	_name = 'odt.medios.revista'

	revista_id = fields.Many2one('odt.medios')
	tamano = fields.Selection([('1','Página'),('2','Página impar'),('3','Spread'),('4','Cuarta de forros'),('5','Tercera de forros'),('6','Otro')],string='Tamaño de Inserción Regular')
	tipo = fields.Selection([('1','Publireportaje'),('2','Gatefold'),('3','Encarte'),('4','Suajes'),('5','Fajilla'),('6','Otro')],string='Tipo')
	titulo = fields.Char(string='Título')
	observaciones = fields.Char(string='Observaciones')

class TablaRadio(models.Model):
	_name = 'odt.medios.radio'

	radio_id = fields.Many2one('odt.medios')
	plaza = fields.Char(string='Plaza')
	tipo = fields.Selection([('1','Spoteo'),('2','Manción 1'),('3','Cápsula 1'),('4','Patrocinio'),('5','Enlaces'),('6','Entrevista'),('7','Otro')],string='Tipo*')
	duracionn = fields.Selection([('1','10"'),('2','20"'),('3','30"'),('4','40"'),('5','50"'),('6','60"')], string='Duración de spot', track_visibility=True)

class TablaPlaza(models.Model):
	_name = 'odt.medios.plaza'

	plazas_id = fields.Many2one('odt.medios',ondelete='cascade')
	plaza = fields.Char(string='Plaza(s)')
	tipo_accion = fields.Char(string='Tipo de Acción')

class inheritContacts(models.Model):
	_inherit = 'res.partner'

	marca_count = fields.Integer(string='marca',compute='_compute_marca_count')

	@api.one
	def _compute_marca_count(self):
		count = self.env['crm.marca']
		self.marca_count = count.search_count([('partner_marca_id', '=', self.id)])

class Marca(models.Model):
	_name = 'crm.marca'
	_description = 'Campo dedicado para las multiples marcas que puede tener una empresa'

	name = fields.Char(string='Nombre de la marca')
	partner_marca_id = fields.Many2one('res.partner',string='Partner', invisible=True)

class TablaGastos(models.Model):
	_inherit = 'project.project'

	tabla_gastos = fields.One2many('project.gastos','gastos_id')
	ref_project = fields.Many2one('crm.lead',string='Proyecto', compute='get_sale_order_reference')
	fin_clave = fields.Char(string='CLAVE')
	u_bruta_p = fields.Float(string='U. Bruta P', compute='_compute_saldo_autorizado')
	u_bruta_r = fields.Float(string='U. Bruta R',compute='_compute_bruta_real')
	dates = fields.Date(related='ref_project.date_deadline', string='Fecha')
	ref_customer = fields.Many2one(related='partner_id', string='Cliente')
	total_pagar = fields.Float(string='I.Planificado', compute='get_sale_order_total')
	saldo_autorizado = fields.Float(string='saldo autorizado', compute='_compute_saldo_autorizado')
	i_facturado = fields.Float(string='I.Facturado', compute='_compute_facturado')

	# Campos de presupuesto autorizado
	btl = fields.Float(related='ref_project.btl', string='BTL/PDV')
	produccion = fields.Float(related='ref_project.produccion', tring='Produccion')
	diseño_creatividad = fields.Float(related='ref_project.diseño_creatividad', string='Diseño')
	gestoria_logistica = fields.Float(related='ref_project.gestoria_logistica', string='Gestoria')
	call_center = fields.Float(related='ref_project.call_center', string='Contact Center')
	digital = fields.Float(related='ref_project.digital', string='Marketing Digital')
	medios = fields.Float(related='ref_project.medios', string='Medios')
	logistica = fields.Float(related='ref_project.logistica', string='Logistica')
	estrategia = fields.Float(related='ref_project.estrategia', string='Estrategia')
	otros_gastos = fields.Float(related='ref_project.otros_gastos',string='Otros')


	@api.one
	def get_sale_order_reference(self):
		for rec in self:
			res = rec.env['sale.order'].search([('id', '=', self.sale_order_id.id)], limit=1)
			rec.ref_project = res.opportunity_id.id

	@api.one
	def get_sale_order_total(self):
		for rec in self:
			res = rec.env['sale.order'].search([('id', '=', self.sale_order_id.id)], limit=1)
			rec.total_pagar = float(res.amount_untaxed)



# planificado es total a cobrar -los gastos autorizados
	@api.one
	@api.depends('u_bruta_r')
	def _compute_bruta_real(self):
			analytic_lines = self.env['account.analytic.line']
			search_account = analytic_lines.search([('account_id','=',self.analytic_account_id.id)])
			self.u_bruta_r = sum(search_account.mapped('amount'))

	@api.one
	@api.depends('ref_project','saldo_autorizado','u_bruta_p')
	def _compute_saldo_autorizado(self):
		if self.ref_project:
			self.saldo_autorizado = (self.ref_project.btl + self.ref_project.produccion + self.ref_project.diseño_creatividad + self.ref_project.call_center + self.ref_project.digital + self.ref_project.medios + self.ref_project.logistica + self.ref_project.gestoria_logistica)
			self.u_bruta_p = (self.total_pagar - self.saldo_autorizado)

	@api.one
	@api.depends('i_facturado')
	def _compute_facturado(self):
		sale_model = self.env['sale.order']
		seach_amount_invoiced = sale_model.search([('invoice_status','=','invoiced'),('analytic_account_id','=',self.analytic_account_id.id)])
		self.i_facturado = sum(seach_amount_invoiced.mapped('amount_untaxed'))


class ColumnasSaleOrder(models.Model):
	_inherit = 'sale.order.line'

	tipo_gasto = fields.Selection([('1','BTL/PDV'),('2','Produccion'),('3','Diseño'),('4','Gestoria'),('5','Contact Center'),('6','Marketing Digital'),('7','Medios'),('8','Logistica'),('9','Estrategia')], string='Area Gasto')
	
class ColumnasPresupuesto(models.Model):
	"""docstring for ColumnasPresupuesto"""
	_inherit = 'crossovered.budget.lines'

	detalle_pres = fields.Char(string='Detalle')
	area = fields.Many2one('odt.areas',string='Area')
	departamento = fields.Many2many('odt.tags.depts',string='Departamento')

class Areas(models.Model):
	"""docstring for Areas"""
	_name = 'odt.areas'

	name = fields.Char(string='Nombre del Area')

class TagsPresupuesto(models.Model):
	_name = 'odt.tags.depts'

	name = fields.Char(string='Departamento')


class Gastos(models.Model):
	"""docstring for Gastos"""
	_name = 'project.gastos'


	gastos_id = fields.Many2one('project.project')
	fac_gastos = fields.Float(string='Gastos Facturados',compute='_sutotal_btl')
	disviacion = fields.Float(string='Desviacion',compute='_sutotal_btl')
	etiqueta_analitica = fields.Many2many('account.analytic.tag', string='Etiqueta')

	btl = fields.Float(related='gastos_id.btl', string='BTL/PDV')
	produccion = fields.Float(related='gastos_id.produccion', tring='Produccion')
	diseño_creatividad = fields.Float(related='gastos_id.diseño_creatividad', string='Diseño')
	gestoria_logistica = fields.Float(related='gastos_id.gestoria_logistica', string='Gestoria')
	call_center = fields.Float(related='gastos_id.call_center', string='Contact Center')
	digital = fields.Float(related='gastos_id.digital', string='Marketing Digital')
	medios = fields.Float(related='gastos_id.medios', string='Medios')
	logistica = fields.Float(related='gastos_id.logistica', string='Logistica')
	estrategia = fields.Float(related='gastos_id.estrategia', string='Estrategia')


	@api.one
	@api.depends('etiqueta_analitica','fac_gastos','disviacion')
	def _sutotal_btl(self):
		analytic_lines = self.env['account.analytic.line']
		analytic_tags_btl = self.env['account.analytic.tag'].search([('name','=','BTL/PDV')])
		analytic_tags_produccion = self.env['account.analytic.tag'].search([('name','=','Producción')])
		analytic_tags_diseno = self.env['account.analytic.tag'].search([('name','=','Diseño')])
		analytic_tags_gestoria = self.env['account.analytic.tag'].search([('name','=','Gestoria')])
		analytic_tags_contact = self.env['account.analytic.tag'].search([('name','=','Contact Center')])
		analytic_tags_marketing = self.env['account.analytic.tag'].search([('name','=','Marketing Digital')])
		analytic_tags_medios = self.env['account.analytic.tag'].search([('name','=','Medios')])
		analytic_tags_logistica = self.env['account.analytic.tag'].search([('name','=','Logistica')])
		analytic_tags_estrategia = self.env['account.analytic.tag'].search([('name','=','Estrategia')])
		search_account = analytic_lines.search([('account_id','=',self.gastos_id.analytic_account_id.id),('tag_ids','in',self.etiqueta_analitica.id)])
		self.fac_gastos = (-(sum(search_account.mapped('amount'))))

		if self.etiqueta_analitica == analytic_tags_btl:
			self.disviacion = self.btl - self.fac_gastos

		if self.etiqueta_analitica == analytic_tags_produccion:
			self.disviacion = self.produccion - self.fac_gastos

		if self.etiqueta_analitica == analytic_tags_diseno:
			self.disviacion = self.diseño_creatividad - self.fac_gastos

		if self.etiqueta_analitica == analytic_tags_gestoria:
			self.disviacion = self.gestoria_logistica - self.fac_gastos

		if self.etiqueta_analitica == analytic_tags_contact:
			self.disviacion = self.call_center - self.fac_gastos

		if self.etiqueta_analitica == analytic_tags_marketing:
			self.disviacion = self.digital - self.fac_gastos

		if self.etiqueta_analitica == analytic_tags_medios:
			self.disviacion = self.medios - self.fac_gastos

		if self.etiqueta_analitica == analytic_tags_logistica:
			self.disviacion = self.logistica - self.fac_gastos

		if self.etiqueta_analitica == analytic_tags_estrategia:
			self.disviacion = self.estrategia - self.fac_gastos
